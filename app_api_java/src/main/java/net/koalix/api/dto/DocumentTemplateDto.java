package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Metadata plus sub-resource URLs for a {@code DocumentTemplate}.
 *
 * <p>The asset URLs ({@code xslHref}, {@code fopConfigHref}, {@code logoHref})
 * are Django endpoints that respond with HTTP 302 to a short-lived presigned
 * S3 URL. Follow the redirect manually — do not carry the caller's OIDC token
 * to S3.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record DocumentTemplateDto(
        Long id,
        String title,
        String xslHref,
        String fopConfigHref,
        String logoHref
) {
}
