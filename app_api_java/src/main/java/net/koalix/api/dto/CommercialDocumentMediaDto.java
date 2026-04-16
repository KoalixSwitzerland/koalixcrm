package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.OffsetDateTime;

/**
 * Mirrors {@code koalixcrm.contracts.models.commercial_document_media.CommercialDocumentMedia}.
 *
 * <p>The worker POSTs an instance here after uploading the rendered PDF.
 * Only the fields on the right of {@code id} are writable.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record CommercialDocumentMediaDto(
        Long id,
        Long commercialDocument,
        Long pdfExportProcess,
        String s3Url,
        String s3Key,
        String status,
        String mediaType,
        Long createdBy,
        OffsetDateTime createdAt,
        OffsetDateTime lastUpdatedAt
) {
}
