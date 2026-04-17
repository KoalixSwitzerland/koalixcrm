package net.koalix.pdf.template;

import com.github.tomakehurst.wiremock.WireMockServer;
import net.koalix.api.CrmApiClient;
import net.koalix.api.dto.DocumentTemplateDto;
import net.koalix.pdf.support.StaticTokenProvider;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.web.reactive.function.client.WebClient;
import org.testcontainers.containers.localstack.LocalStackContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;
import reactor.netty.http.client.HttpClient;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.S3Configuration;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.GetObjectPresignRequest;
import software.amazon.awssdk.services.s3.presigner.model.PresignedGetObjectRequest;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.nio.file.Files;
import java.time.Duration;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.get;
import static com.github.tomakehurst.wiremock.client.WireMock.urlPathEqualTo;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatNoException;

/**
 * Step 1 of the pdf-export-service integration-test plan
 * (see INTEGRATION_TEST_CONCEPT.md).
 *
 * <p>Exercises {@link TemplateFetcher} end-to-end over real infrastructure:
 * template assets are uploaded to LocalStack S3, Django is simulated by
 * WireMock returning {@code 302 Location: <presigned URL>}, and the fetcher
 * must produce three local files on disk.
 */
@Testcontainers
class TemplateFetcherIT {

    private static final String BUCKET = "pdf-templates-it";
    private static final DockerImageName LOCALSTACK_IMAGE =
            DockerImageName.parse("localstack/localstack:3.8");

    @Container
    static final LocalStackContainer LOCALSTACK = new LocalStackContainer(LOCALSTACK_IMAGE)
            .withServices(LocalStackContainer.Service.S3);

    private static S3Client s3;
    private static S3Presigner presigner;
    private static WireMockServer wireMock;

    private TemplateFetcher fetcher;

    @BeforeAll
    static void bootstrapInfra() throws IOException {
        URI endpoint = LOCALSTACK.getEndpointOverride(LocalStackContainer.Service.S3);
        var creds = StaticCredentialsProvider.create(AwsBasicCredentials.create(
                LOCALSTACK.getAccessKey(), LOCALSTACK.getSecretKey()));

        s3 = S3Client.builder()
                .endpointOverride(endpoint)
                .credentialsProvider(creds)
                .region(Region.of(LOCALSTACK.getRegion()))
                .serviceConfiguration(S3Configuration.builder().pathStyleAccessEnabled(true).build())
                .build();
        presigner = S3Presigner.builder()
                .endpointOverride(endpoint)
                .credentialsProvider(creds)
                .region(Region.of(LOCALSTACK.getRegion()))
                .serviceConfiguration(S3Configuration.builder().pathStyleAccessEnabled(true).build())
                .build();

        s3.createBucket(CreateBucketRequest.builder().bucket(BUCKET).build());

        putFixture("templatefiles/invoice.xsl",   "/fixtures/templates/invoice.xsl");
        putFixture("templatefiles/fop.xconf",     "/fixtures/fop/fop.xconf");
        putFixture("templatefiles/logo.jpg",      "/fixtures/s3/logo.jpg");

        wireMock = new WireMockServer(wireMockConfig().dynamicPort());
        wireMock.start();
    }

    @AfterAll
    static void shutdownInfra() {
        if (wireMock != null) {
            wireMock.stop();
        }
        if (s3 != null) {
            s3.close();
        }
        if (presigner != null) {
            presigner.close();
        }
    }

    @BeforeEach
    void wireFetcher() {
        // Reactor-Netty WebClient that does NOT follow 302 — we need to read
        // the Location header ourselves. S3 presigned URLs we fetch directly
        // with no redirect in the way.
        WebClient noRedirect = WebClient.builder()
                .clientConnector(new ReactorClientHttpConnector(
                        HttpClient.create().followRedirect(false)))
                .build();
        CrmApiClient crm = new CrmApiClient(
                noRedirect,
                new StaticTokenProvider("test-token"),
                wireMock.baseUrl(),
                null, null);
        fetcher = new TemplateFetcher(crm, noRedirect);
    }

    @AfterEach
    void resetStubs() {
        wireMock.resetAll();
    }

    @Test
    void fetchesAllThreeAssets_whenAllHrefsProvided() throws Exception {
        stub302("/document_templates/1/xsl/",        "templatefiles/invoice.xsl");
        stub302("/document_templates/1/fop-config/", "templatefiles/fop.xconf");
        stub302("/document_templates/1/logo/",       "templatefiles/logo.jpg");

        DocumentTemplateDto dto = new DocumentTemplateDto(
                1L, "Invoice EN",
                "/document_templates/1/xsl/",
                "/document_templates/1/fop-config/",
                "/document_templates/1/logo/");

        TemplateAssets assets = fetcher.fetch(dto);

        assertThat(assets.xslFile()).isNotNull();
        assertThat(Files.size(assets.xslFile())).isGreaterThan(1_000L);
        assertThat(Files.readString(assets.xslFile())).startsWith("<?xml");

        assertThat(assets.fopConfigFile()).isNotNull();
        assertThat(Files.size(assets.fopConfigFile())).isGreaterThan(500L);

        assertThat(assets.logoFile()).isNotNull();
        assertThat(Files.size(assets.logoFile())).isGreaterThan(100L);
    }

    @Test
    void skipsOptionalAssets_whenHrefsAreNull() throws Exception {
        stub302("/document_templates/2/xsl/", "templatefiles/invoice.xsl");

        DocumentTemplateDto dto = new DocumentTemplateDto(
                2L, "Invoice (no logo, no fop config)",
                "/document_templates/2/xsl/",
                null,
                null);

        TemplateAssets assets = fetcher.fetch(dto);

        assertThat(assets.xslFile()).isNotNull();
        assertThat(assets.fopConfigFile()).isNull();
        assertThat(assets.logoFile()).isNull();
    }

    @Test
    void treatsOptionalAssetAsNull_whenDjangoReturns404() throws Exception {
        stub302("/document_templates/3/xsl/", "templatefiles/invoice.xsl");
        wireMock.stubFor(get(urlPathEqualTo("/document_templates/3/logo/"))
                .willReturn(aResponse().withStatus(404)));

        DocumentTemplateDto dto = new DocumentTemplateDto(
                3L, "Invoice (logo 404)",
                "/document_templates/3/xsl/",
                null,
                "/document_templates/3/logo/");

        TemplateAssets assets;
        try {
            assets = fetcher.fetch(dto);
        } catch (Exception e) {
            throw new AssertionError("fetcher must not throw on optional-asset 404", e);
        }

        assertThat(assets.logoFile()).isNull();
        assertThat(assets.xslFile()).isNotNull();
    }

    @Test
    void requiredAsset404_surfacesAsException() {
        wireMock.stubFor(get(urlPathEqualTo("/document_templates/4/xsl/"))
                .willReturn(aResponse().withStatus(404)));

        DocumentTemplateDto dto = new DocumentTemplateDto(
                4L, "Invoice (xsl 404)",
                "/document_templates/4/xsl/", null, null);

        assertThatNoException().isThrownBy(() -> {
            // sanity: stub is reachable
            wireMock.baseUrl();
        });
        // A missing required asset MUST surface — the orchestrator relies on
        // this to mark the process row as failed. We don't pin the exception
        // type (WebClientResponseException today), only that something throws.
        try {
            fetcher.fetch(dto);
            throw new AssertionError("expected fetch() to throw when required XSL is missing");
        } catch (Exception expected) {
            assertThat(expected).isNotNull();
        }
    }

    // --- helpers ------------------------------------------------------------

    private void stub302(String urlPath, String s3Key) {
        wireMock.stubFor(get(urlPathEqualTo(urlPath))
                .willReturn(aResponse()
                        .withStatus(302)
                        .withHeader("Location", presignedUrl(s3Key))));
    }

    private String presignedUrl(String key) {
        PresignedGetObjectRequest req = presigner.presignGetObject(
                GetObjectPresignRequest.builder()
                        .signatureDuration(Duration.ofMinutes(5))
                        .getObjectRequest(b -> b.bucket(BUCKET).key(key))
                        .build());
        return req.url().toString();
    }

    private static void putFixture(String s3Key, String classpathResource) throws IOException {
        try (InputStream in = TemplateFetcherIT.class.getResourceAsStream(classpathResource)) {
            if (in == null) {
                throw new IllegalStateException("Fixture missing on classpath: " + classpathResource);
            }
            byte[] bytes = in.readAllBytes();
            s3.putObject(PutObjectRequest.builder().bucket(BUCKET).key(s3Key).build(),
                    RequestBody.fromBytes(bytes));
        }
    }
}
