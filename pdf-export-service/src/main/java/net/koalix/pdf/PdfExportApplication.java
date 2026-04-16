package net.koalix.pdf;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.retry.annotation.EnableRetry;

@SpringBootApplication
@EnableRetry
public class PdfExportApplication {
    public static void main(String[] args) {
        SpringApplication.run(PdfExportApplication.class, args);
    }
}
