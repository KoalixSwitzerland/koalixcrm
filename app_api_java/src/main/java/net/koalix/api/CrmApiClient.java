package net.koalix.api;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.CommercialDocumentMediaDto;
import net.koalix.api.dto.DocumentTemplateDto;
import net.koalix.api.dto.PdfExportProcessDto;
import net.koalix.api.dto.PdfExportProcessPatchDto;
import net.koalix.api.dto.UserExtensionDto;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

import java.net.URI;
import java.util.function.Consumer;
import java.util.function.Supplier;

/**
 * Hand-written REST client for the koalixCRM JSON endpoints consumed by the
 * PDF worker. Every call attaches an OIDC bearer token via
 * {@link OidcTokenProvider} and retries once on 401/403 with a freshly-minted
 * token (mirrors {@code koalixcrm/shared/api_client.py}).
 */
public class CrmApiClient {

    private final WebClient webClient;
    private final OidcTokenProvider tokenProvider;
    private final String baseUrl;
    private final String originHeaderName;
    private final String originHeaderValue;
    private final ObjectMapper objectMapper;

    public CrmApiClient(WebClient webClient, OidcTokenProvider tokenProvider, String baseUrl,
                        String originHeaderName, String originHeaderValue) {
        this.webClient = webClient;
        this.tokenProvider = tokenProvider;
        this.baseUrl = baseUrl.replaceAll("/+$", "");
        this.originHeaderName = originHeaderName;
        this.originHeaderValue = originHeaderValue;
        this.objectMapper = new ObjectMapper()
                .registerModule(new JavaTimeModule())
                .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE)
                .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }

    public PdfExportProcessDto getPdfExportProcess(long id) {
        return get("/pdf_export_processes/" + id + "/", PdfExportProcessDto.class);
    }

    public PdfExportProcessDto patchPdfExportProcess(long id, PdfExportProcessPatchDto patch) {
        return patch("/pdf_export_processes/" + id + "/", patch, PdfExportProcessDto.class);
    }

    public DocumentTemplateDto getDocumentTemplate(long id) {
        return get("/document_templates/" + id + "/", DocumentTemplateDto.class);
    }

    public UserExtensionDto getUserExtension(long id) {
        return get("/user_extensions/" + id + "/", UserExtensionDto.class);
    }

    public CommercialDocumentDto getCommercialDocumentNested(String sourceModel, long id) {
        String path = switch (sourceModel) {
            case "Invoice" -> "/invoices/" + id + "/nested/";
            case "Quotation" -> "/quotations/" + id + "/nested/";
            case "DeliveryNote", "DespatchAdvice" -> "/despatch_advices/" + id + "/nested/";
            case "PurchaseOrder" -> "/purchase_orders/" + id + "/nested/";
            case "PaymentReminder" -> "/payment_reminders/" + id + "/nested/";
            case "CreditNote" -> "/credit_notes/" + id + "/nested/";
            default -> throw new IllegalArgumentException("Unsupported source_model: " + sourceModel);
        };
        return get(path, CommercialDocumentDto.class);
    }

    public CommercialDocumentMediaDto createCommercialDocumentMedia(CommercialDocumentMediaDto body) {
        return post("/commercial_document_media/", body, CommercialDocumentMediaDto.class);
    }

    /**
     * Resolve an href returned by the DocumentTemplate endpoints (xsl/fop-config/logo)
     * to its presigned S3 URL. Does NOT follow the redirect — it returns the
     * short-lived S3 URL so the caller can fetch it without the bearer token.
     */
    public URI resolvePresignedAssetUrl(String href) {
        URI uri = URI.create(href.startsWith("http") ? href : baseUrl + href);
        ClientResponse response = webClient.get()
                .uri(uri)
                .headers(authHeaders())
                .exchangeToMono(r -> {
                    if (r.statusCode().is3xxRedirection()) {
                        return Mono.just(r);
                    }
                    return r.createException().flatMap(Mono::error);
                })
                .block();
        if (response == null) {
            throw new IllegalStateException("No response from " + uri);
        }
        String location = response.headers().asHttpHeaders().getFirst(HttpHeaders.LOCATION);
        if (location == null) {
            throw new IllegalStateException("Redirect from " + uri + " had no Location header");
        }
        return URI.create(location);
    }

    // ---- internals ---------------------------------------------------------

    private Consumer<HttpHeaders> authHeaders() {
        return headers -> {
            headers.set(HttpHeaders.AUTHORIZATION, "Bearer " + tokenProvider.accessToken());
            if (originHeaderName != null && originHeaderValue != null) {
                headers.set(originHeaderName, originHeaderValue);
            }
        };
    }

    private <T> T get(String path, Class<T> type) {
        return execute(() -> webClient.get()
                .uri(baseUrl + path)
                .headers(authHeaders())
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block(), type);
    }

    private <T> T post(String path, Object body, Class<T> type) {
        return execute(() -> webClient.post()
                .uri(baseUrl + path)
                .headers(authHeaders())
                .bodyValue(body)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block(), type);
    }

    private <T> T patch(String path, Object body, Class<T> type) {
        return execute(() -> webClient.patch()
                .uri(baseUrl + path)
                .headers(authHeaders())
                .bodyValue(body)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block(), type);
    }

    private <T> T execute(Supplier<JsonNode> call, Class<T> type) {
        try {
            JsonNode body = call.get();
            return body == null ? null : objectMapper.convertValue(body, type);
        } catch (WebClientResponseException e) {
            if (e.getStatusCode() == HttpStatus.UNAUTHORIZED || e.getStatusCode() == HttpStatus.FORBIDDEN) {
                tokenProvider.refresh();
                JsonNode body = call.get();
                return body == null ? null : objectMapper.convertValue(body, type);
            }
            throw e;
        }
    }
}
