package net.koalix.pdf.sqs;

public record PdfExportEnvelope(String type, PdfExportCommand payload) {
}
