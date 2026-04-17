package net.koalix.pdf.template;

import net.koalix.api.CrmApiClient;
import net.koalix.api.dto.DocumentTemplateDto;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Downloads the XSL, FOP config and logo that belong to a {@link DocumentTemplateDto}
 * into a freshly-created temp directory.
 *
 * <p>The Django endpoints return HTTP 302 to a short-lived presigned S3 URL.
 * We first resolve the presigned URL via {@link CrmApiClient#resolvePresignedAssetUrl}
 * (bearer token attached), then fetch the S3 URL anonymously.
 */
@Component
public class TemplateFetcher {

    private final CrmApiClient crm;
    private final WebClient webClient;

    public TemplateFetcher(CrmApiClient crm, WebClient webClient) {
        this.crm = crm;
        this.webClient = webClient;
    }

    public TemplateAssets fetch(DocumentTemplateDto template) throws IOException {
        Path tempDir = Files.createTempDirectory("pdf-tpl-" + template.id() + "-");
        Path xsl = downloadRequired(template.xslHref(), tempDir.resolve("template.xsl"));
        Path fopConfig = downloadOptional(template.fopConfigHref(), tempDir.resolve("fop.xconf"));
        Path logo = downloadOptional(template.logoHref(), tempDir.resolve("logo"));
        return new TemplateAssets(xsl, fopConfig, logo);
    }

    private Path downloadRequired(String href, Path target) throws IOException {
        if (href == null) {
            throw new IllegalStateException("Required template asset href missing: " + target);
        }
        return download(href, target);
    }

    private Path downloadOptional(String href, Path target) throws IOException {
        if (href == null) {
            return null;
        }
        try {
            return download(href, target);
        } catch (org.springframework.web.reactive.function.client.WebClientResponseException.NotFound e) {
            return null;
        }
    }

    private Path download(String href, Path target) throws IOException {
        URI presigned = crm.resolvePresignedAssetUrl(href);
        byte[] bytes = webClient.get()
                .uri(presigned)
                .retrieve()
                .bodyToMono(byte[].class)
                .block();
        if (bytes == null) {
            throw new IOException("Empty body for " + presigned);
        }
        Files.write(target, bytes);
        return target;
    }
}
