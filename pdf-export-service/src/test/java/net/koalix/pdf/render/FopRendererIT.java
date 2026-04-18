package net.koalix.pdf.render;

import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.UserExtensionDto;
import net.koalix.pdf.support.DocumentFixtures;
import net.koalix.pdf.template.TemplateAssets;
import net.koalix.pdf.xml.XmlAggregator;
import net.koalix.pdf.xml.builders.CommercialDocumentXmlBuilder;
import net.koalix.pdf.xml.builders.PartyXmlBuilder;
import net.koalix.pdf.xml.builders.PositionXmlBuilder;
import net.koalix.pdf.xml.builders.UserExtensionXmlBuilder;
import org.apache.fop.apps.FopFactory;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Locale;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Step 2 of the pdf-export-service integration-test plan
 * (see INTEGRATION_TEST_CONCEPT.md).
 *
 * <p>Feeds the current {@code <koalixcrm-export>} XML shape through every
 * real XSL template bundled under
 * {@code src/test/resources/fixtures/templates/}. The assertion is
 * deliberately loose — a valid PDF byte-stream is good enough. Blank pages
 * are the expected outcome until the XSL-reconciliation work in planned
 * step #4 of {@code CELERY_TO_JAVA_MIGRATION.md} lands.
 *
 * <p>The rendered PDF size is printed so a future PR can diff against it
 * once reconciliation adds real layout.
 */
class FopRendererIT {

    @TempDir
    static Path sharedTempDir;

    private static Path fopBaseDir;
    private static FopFactory fopFactory;
    private static XmlAggregator aggregator;
    private static FopRenderer renderer;

    @BeforeAll
    static void bootstrap() throws Exception {
        fopBaseDir = sharedTempDir.resolve("fop-base");
        Files.createDirectories(fopBaseDir);

        copyClasspath("/fixtures/fop/fop.xconf",            fopBaseDir.resolve("fop.xconf"));
        copyClasspath("/fixtures/fop/DejaVuSans.ttf",        fopBaseDir.resolve("DejaVuSans.ttf"));
        copyClasspath("/fixtures/fop/DejaVuSans-Bold.ttf",   fopBaseDir.resolve("DejaVuSans-Bold.ttf"));
        copyClasspath("/fixtures/fop/dejavusans.xml",        fopBaseDir.resolve("dejavusans.xml"));
        copyClasspath("/fixtures/fop/dejavusans-bold.xml",   fopBaseDir.resolve("dejavusans-bold.xml"));

        try (InputStream conf = Files.newInputStream(fopBaseDir.resolve("fop.xconf"))) {
            fopFactory = FopFactory.newInstance(fopBaseDir.toUri(), conf);
        }

        aggregator = new XmlAggregator(
                new CommercialDocumentXmlBuilder(new PartyXmlBuilder(), new PositionXmlBuilder()),
                new UserExtensionXmlBuilder());
        renderer = new FopRenderer(fopFactory);
    }

    // Scope note: balancesheet.xsl and profitlossstatement.xsl are intentionally
    // excluded. Their XSL root is koalixaccountingbalacesheet /
    // koalixaccountingprofitlossstatement — they render from a different data
    // aggregate than <koalixcrm-export>. They belong to the accounting-export
    // flow, which is not yet migrated; once it is, it deserves its own IT.
    @ParameterizedTest(name = "renders {0} without exception")
    @ValueSource(strings = {
            "invoice.xsl",
            "quote.xsl",
            "deliveryorder.xsl",
            "purchaseorder.xsl",
            "purchaseconfirmation.xsl",
            "koalix_invoice_20180518.xsl",
            "acme_quote.xsl",
            "sample_quote_20210412.xsl",
            "project_report.xsl",
            "project_report_acme.xsl",
            "project_report_actual_effort_acme.xsl",
            "work_report.xsl",
    })
    void rendersWithKoalixcrmExportShape(String templateFileName) throws Exception {
        CommercialDocumentDto doc = DocumentFixtures.invoice();
        UserExtensionDto user = DocumentFixtures.userExtension();
        byte[] xml = aggregator.build(doc, user);

        Path xslCopy = fopBaseDir.resolve(templateFileName);
        copyClasspath("/fixtures/templates/" + templateFileName, xslCopy);
        TemplateAssets assets = new TemplateAssets(xslCopy, fopBaseDir.resolve("fop.xconf"), null);

        byte[] pdf = renderer.render(xml, assets);

        assertThat(pdf).isNotNull();
        assertThat(pdf.length).isGreaterThan(0);
        String header = new String(pdf, 0, Math.min(5, pdf.length), StandardCharsets.US_ASCII);
        assertThat(header)
                .as("first 5 bytes should be a PDF signature for template " + templateFileName)
                .isEqualTo("%PDF-");

        Path outDir = Path.of("build", "test-output", "pdfs");
        Files.createDirectories(outDir);
        Path outFile = outDir.resolve(templateFileName.replace(".xsl", ".pdf"));
        Files.write(outFile, pdf);

        // Signal bytes for humans scanning the CI log. Not an assertion.
        System.out.printf(Locale.ROOT, "[FopRendererIT] %-50s pdf=%,8d bytes  -> %s%n",
                templateFileName, pdf.length, outFile.toAbsolutePath());
    }

    private static void copyClasspath(String resource, Path target) throws Exception {
        try (InputStream in = FopRendererIT.class.getResourceAsStream(resource)) {
            if (in == null) {
                throw new IllegalStateException("Fixture missing on classpath: " + resource);
            }
            Files.copy(in, target, StandardCopyOption.REPLACE_EXISTING);
        }
    }
}
