package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Partial-update payload for {@code PATCH /pdf_export_processes/{id}/}. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PdfExportProcessPatchDto(String status, String resultUrl, String errorMessage) {
}
