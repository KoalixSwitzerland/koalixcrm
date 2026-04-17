package net.koalix.pdf.render;

import net.koalix.pdf.template.TemplateAssets;
import org.apache.fop.apps.Fop;
import org.apache.fop.apps.FopFactory;
import org.apache.fop.apps.MimeConstants;
import org.springframework.stereotype.Component;

import javax.xml.XMLConstants;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.sax.SAXResult;
import javax.xml.transform.stream.StreamSource;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

/**
 * Runs Apache FOP in-process: XSL-FO XML + XSL stylesheet → PDF bytes.
 *
 * <p>Replaces the previous subprocess call to {@code /usr/bin/fop}.
 * {@link FopFactory} is a Spring bean so base-URI and config resolution stay
 * centralised.
 */
@Component
public class FopRenderer {

    private final FopFactory fopFactory;

    public FopRenderer(FopFactory fopFactory) {
        this.fopFactory = fopFactory;
    }

    public byte[] render(byte[] xmlDocument, TemplateAssets assets) throws Exception {
        try (InputStream xml = new ByteArrayInputStream(xmlDocument);
             InputStream xsl = java.nio.file.Files.newInputStream(assets.xslFile());
             ByteArrayOutputStream out = new ByteArrayOutputStream()) {

            Fop fop = fopFactory.newFop(MimeConstants.MIME_PDF, out);
            TransformerFactory tFactory = TransformerFactory.newInstance();
            tFactory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
            tFactory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
            tFactory.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");
            Transformer transformer = tFactory.newTransformer(new StreamSource(xsl));
            transformer.transform(new StreamSource(xml), new SAXResult(fop.getDefaultHandler()));
            return out.toByteArray();
        }
    }
}
