package net.koalix.pdf.storage;

import net.koalix.pdf.config.AppProperties;
import org.springframework.stereotype.Component;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.net.URI;

/**
 * Uploads rendered PDF bytes to the configured S3 bucket.
 *
 * <p>Key format is identical to the Python worker
 * ({@code pdf-exports/<model>_<id>_<process_id>.pdf}) so downstream consumers
 * don't notice the rewrite.
 */
@Component
public class S3PdfUploader {

    private final S3Client s3Client;
    private final AppProperties props;

    public S3PdfUploader(S3Client s3Client, AppProperties props) {
        this.s3Client = s3Client;
        this.props = props;
    }

    public String keyFor(String sourceModel, long sourceId, long processId) {
        return props.s3().keyPrefix() + "/" + sourceModel + "_" + sourceId + "_" + processId + ".pdf";
    }

    public URI upload(String key, byte[] body) {
        PutObjectRequest request = PutObjectRequest.builder()
                .bucket(props.s3().pdfBucket())
                .key(key)
                .contentType("application/pdf")
                .build();
        s3Client.putObject(request, RequestBody.fromBytes(body));
        java.net.URL url = s3Client.utilities().getUrl(b -> b.bucket(props.s3().pdfBucket()).key(key));
        try {
            return url.toURI();
        } catch (java.net.URISyntaxException e) {
            throw new IllegalStateException("S3 returned non-URI URL: " + url, e);
        }
    }
}
