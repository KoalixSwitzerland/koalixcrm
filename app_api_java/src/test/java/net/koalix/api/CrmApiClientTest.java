package net.koalix.api;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.tomakehurst.wiremock.WireMockServer;
import net.koalix.api.dto.CommercialDocumentMediaDto;
import net.koalix.api.dto.PdfExportProcessDto;
import net.koalix.api.dto.PdfExportProcessPatchDto;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.web.reactive.function.client.WebClient;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.options;
import static org.assertj.core.api.Assertions.assertThat;

class CrmApiClientTest {

    private WireMockServer wireMock;
    private CrmApiClient client;

    @BeforeEach
    void setUp() {
        wireMock = new WireMockServer(options().dynamicPort());
        wireMock.start();

        // Discovery doc so the OIDC provider finds a token endpoint
        wireMock.stubFor(get(urlEqualTo("/realms/koalix/.well-known/openid-configuration"))
                .willReturn(okJson("{\"token_endpoint\":\"" + wireMock.baseUrl() + "/token\"}")));
        wireMock.stubFor(post(urlEqualTo("/token"))
                .willReturn(okJson("{\"access_token\":\"T1\",\"expires_in\":300}")));

        var webClient = WebClient.builder().build();
        var tokens = new OidcTokenProvider(
                wireMock.baseUrl() + "/realms/koalix",
                "pdf-worker", "secret", "",
                webClient, new ObjectMapper());

        client = new CrmApiClient(webClient, tokens, wireMock.baseUrl(), null, null);
    }

    @AfterEach
    void tearDown() {
        wireMock.stop();
    }

    @Test
    void getPdfExportProcess_parsesJson() {
        wireMock.stubFor(get(urlEqualTo("/pdf_export_processes/42/"))
                .willReturn(okJson("""
                        {
                          "id": 42,
                          "source_model": "Invoice",
                          "source_id": 17,
                          "template_set": 3,
                          "triggered_by": 5,
                          "status": "processing",
                          "result_url": "",
                          "error_message": "",
                          "created_at": "2026-04-16T12:34:56Z",
                          "updated_at": "2026-04-16T12:35:10Z"
                        }
                        """)));
        PdfExportProcessDto dto = client.getPdfExportProcess(42L);
        assertThat(dto.id()).isEqualTo(42L);
        assertThat(dto.sourceModel()).isEqualTo("Invoice");
        assertThat(dto.status()).isEqualTo("processing");
    }

    @Test
    void patchPdfExportProcess_sendsBodyAndReturnsDto() {
        wireMock.stubFor(patch(urlEqualTo("/pdf_export_processes/42/"))
                .willReturn(okJson("""
                        {"id":42,"source_model":"Invoice","source_id":17,"status":"completed"}
                        """)));

        PdfExportProcessDto dto = client.patchPdfExportProcess(
                42L, new PdfExportProcessPatchDto("completed", "http://s3/x.pdf", null));

        assertThat(dto.status()).isEqualTo("completed");
        wireMock.verify(patchRequestedFor(urlEqualTo("/pdf_export_processes/42/"))
                .withHeader("Authorization", equalTo("Bearer T1"))
                .withRequestBody(matchingJsonPath("$.status", equalTo("completed"))));
    }

    @Test
    void createMedia_postsJson() {
        wireMock.stubFor(post(urlEqualTo("/commercial_document_media/"))
                .willReturn(aResponse().withStatus(201).withHeader("Content-Type", "application/json")
                        .withBody("""
                                {"id":101,"commercial_document":17,"s3_url":"http://s3/x.pdf","status":"completed"}
                                """)));

        CommercialDocumentMediaDto body = new CommercialDocumentMediaDto(
                null, 17L, 42L, "http://s3/x.pdf", "pdf-exports/x.pdf",
                "completed", "application/pdf", null, null, null);

        CommercialDocumentMediaDto created = client.createCommercialDocumentMedia(body);

        assertThat(created.id()).isEqualTo(101L);
    }

    @Test
    void retriesOnce_on401() {
        // first call fails, refresh, second call succeeds
        wireMock.stubFor(get(urlEqualTo("/pdf_export_processes/7/"))
                .inScenario("auth")
                .whenScenarioStateIs(com.github.tomakehurst.wiremock.stubbing.Scenario.STARTED)
                .willReturn(aResponse().withStatus(401))
                .willSetStateTo("retried"));
        wireMock.stubFor(get(urlEqualTo("/pdf_export_processes/7/"))
                .inScenario("auth")
                .whenScenarioStateIs("retried")
                .willReturn(okJson("{\"id\":7,\"source_model\":\"Invoice\",\"source_id\":1,\"status\":\"pending\"}")));

        PdfExportProcessDto dto = client.getPdfExportProcess(7L);
        assertThat(dto.id()).isEqualTo(7L);
    }
}
