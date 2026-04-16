package net.koalix.pdf.orchestrator;

import net.koalix.api.CrmApiClient;
import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.CommercialDocumentMediaDto;
import net.koalix.api.dto.DocumentTemplateDto;
import net.koalix.api.dto.PdfExportProcessDto;
import net.koalix.api.dto.PdfExportProcessPatchDto;
import net.koalix.api.dto.UserExtensionDto;
import net.koalix.pdf.render.FopRenderer;
import net.koalix.pdf.sqs.PdfExportCommand;
import net.koalix.pdf.storage.S3PdfUploader;
import net.koalix.pdf.template.TemplateAssets;
import net.koalix.pdf.template.TemplateFetcher;
import net.koalix.pdf.xml.XmlAggregator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Recover;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;

import java.net.URI;

/**
 * End-to-end orchestration of a single PDF export job.
 *
 * <p>Retry policy mirrors the Celery worker: 3 attempts, exponential backoff
 * capped at 30 s. Terminal failure PATCHes the process row to {@code failed}
 * and the SQS message is acked anyway — Spring Cloud AWS moves it to the DLQ
 * once redrive policy is exhausted.
 */
@Component
public class PdfExportOrchestrator {

    private static final Logger LOG = LoggerFactory.getLogger(PdfExportOrchestrator.class);

    private final CrmApiClient crm;
    private final TemplateFetcher templateFetcher;
    private final XmlAggregator xmlAggregator;
    private final FopRenderer renderer;
    private final S3PdfUploader uploader;

    public PdfExportOrchestrator(CrmApiClient crm, TemplateFetcher templateFetcher,
                                 XmlAggregator xmlAggregator, FopRenderer renderer,
                                 S3PdfUploader uploader) {
        this.crm = crm;
        this.templateFetcher = templateFetcher;
        this.xmlAggregator = xmlAggregator;
        this.renderer = renderer;
        this.uploader = uploader;
    }

    @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000, multiplier = 2, maxDelay = 30_000))
    public void handle(PdfExportCommand cmd) throws Exception {
        LOG.info("Starting PDF export process_id={} source_model={} source_id={}",
                cmd.processId(), cmd.sourceModel(), cmd.sourceId());

        if (cmd.templateSetId() == 0L) {
            throw new IllegalStateException(
                    "template_set_id is 0 (not set) for process_id=" + cmd.processId());
        }

        crm.patchPdfExportProcess(cmd.processId(),
                new PdfExportProcessPatchDto("processing", null, null));

        PdfExportProcessDto process = crm.getPdfExportProcess(cmd.processId());
        CommercialDocumentDto document = crm.getCommercialDocumentNested(cmd.sourceModel(), cmd.sourceId());
        DocumentTemplateDto template = crm.getDocumentTemplate(cmd.templateSetId());
        UserExtensionDto userExtension = document.userExtension() != null
                ? crm.getUserExtension(document.userExtension())
                : null;

        TemplateAssets assets = templateFetcher.fetch(template);
        byte[] xmlDocument = xmlAggregator.build(document, userExtension);
        byte[] pdf = renderer.render(xmlDocument, assets);

        String s3Key = uploader.keyFor(cmd.sourceModel(), cmd.sourceId(), cmd.processId());
        URI s3Url = uploader.upload(s3Key, pdf);

        CommercialDocumentMediaDto media = new CommercialDocumentMediaDto(
                null,
                cmd.sourceId(),
                cmd.processId(),
                s3Url.toString(),
                s3Key,
                "completed",
                "application/pdf",
                cmd.printedByUserId() == 0 ? null : cmd.printedByUserId(),
                null,
                null);
        crm.createCommercialDocumentMedia(media);

        crm.patchPdfExportProcess(cmd.processId(),
                new PdfExportProcessPatchDto("completed", s3Url.toString(), null));

        LOG.info("PDF export complete process_id={} url={} (fetched process status={})",
                cmd.processId(), s3Url, process.status());
    }

    @Recover
    public void recover(Exception ex, PdfExportCommand cmd) {
        LOG.error("Terminal failure for process_id={}: {}", cmd.processId(), ex.toString(), ex);
        crm.patchPdfExportProcess(cmd.processId(),
                new PdfExportProcessPatchDto("failed", null, ex.toString()));
    }
}
