package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.OffsetDateTime;

/**
 * Mirrors {@code koalixcrm.core.models.pdf_export_process.PDFExportProcess}.
 *
 * <p>Writable fields (PATCH): {@code status}, {@code resultUrl},
 * {@code errorMessage}. All other fields are populated by the Django producer
 * when the export job is enqueued and must not be changed by the worker.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PdfExportProcessDto(
        Long id,
        String sourceModel,
        Long sourceId,
        Long templateSet,
        Long triggeredBy,
        String status,
        String resultUrl,
        String errorMessage,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
