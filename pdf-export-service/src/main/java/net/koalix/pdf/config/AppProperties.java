package net.koalix.pdf.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Typed configuration for {@code pdf-export-service}.
 *
 * <p>The {@code oidc} and {@code crm} sections mirror the env-var names
 * used by the Python {@code api_client.py} so ops keeps a single source of
 * truth across worker rewrites.
 */
@ConfigurationProperties(prefix = "koalixcrm")
public record AppProperties(
        Crm crm,
        Oidc oidc,
        S3 s3,
        Sqs sqs,
        Origin origin
) {
    public record Crm(String baseUrl) {}

    public record Oidc(String issuer, String clientId, String clientSecret, String scope) {}

    public record S3(String pdfBucket, String keyPrefix) {
        public S3 {
            if (keyPrefix == null) {
                keyPrefix = "pdf-exports";
            }
        }
    }

    public record Sqs(String queueName) {}

    public record Origin(boolean enabled, String headerName, String headerValue) {
        public Origin {
            if (headerName == null) {
                headerName = "X-Custom-Origin-Verify";
            }
        }
    }
}
