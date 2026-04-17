package net.koalix.pdf.sqs;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Wire contract — mirrors {@code koalixcrm_mq_commands.pdf_export_command.PDFExportCommand}.
 *
 * <p>Sent by the Django producer on SQS as:
 * <pre>
 * { "type": "PDFExportCommand", "payload": { ... } }
 * </pre>
 *
 * Field conventions (see {@code doc/pdf_creation_service/05-interfaces.md}):
 * <ul>
 *   <li>{@code templateSetId == 0} means "not set" — the worker treats this as an error.</li>
 *   <li>{@code printedByUserId == 0} means "not set".</li>
 * </ul>
 */
public record PdfExportCommand(
        @JsonProperty("process_id") long processId,
        @JsonProperty("source_model") String sourceModel,
        @JsonProperty("source_id") long sourceId,
        @JsonProperty("template_set_id") long templateSetId,
        @JsonProperty("printed_by_user_id") long printedByUserId
) {

    public static final String TYPE = "PDFExportCommand";
}
