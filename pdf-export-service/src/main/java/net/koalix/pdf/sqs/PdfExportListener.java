package net.koalix.pdf.sqs;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.awspring.cloud.sqs.annotation.SqsListener;
import net.koalix.pdf.orchestrator.PdfExportOrchestrator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/**
 * Entry point for SQS messages.
 *
 * <p>Delegates parsing (the message body is the envelope JSON) to Jackson,
 * then hands the payload to {@link PdfExportOrchestrator}. Messages whose
 * {@code type} is not {@code "PDFExportCommand"} are logged and acknowledged
 * so the queue drains — they should never arrive in practice, but the
 * behaviour mirrors the current Python poller.
 */
@Component
public class PdfExportListener {

    private static final Logger LOG = LoggerFactory.getLogger(PdfExportListener.class);

    private final ObjectMapper objectMapper;
    private final PdfExportOrchestrator orchestrator;

    public PdfExportListener(ObjectMapper objectMapper, PdfExportOrchestrator orchestrator) {
        this.objectMapper = objectMapper;
        this.orchestrator = orchestrator;
    }

    @SqsListener("${koalixcrm.sqs.queue-name}")
    public void onMessage(String body) throws Exception {
        PdfExportEnvelope envelope = objectMapper.readValue(body, PdfExportEnvelope.class);
        if (!PdfExportCommand.TYPE.equals(envelope.type())) {
            LOG.warn("Ignoring unsupported envelope type: {}", envelope.type());
            return;
        }
        orchestrator.handle(envelope.payload());
    }
}
