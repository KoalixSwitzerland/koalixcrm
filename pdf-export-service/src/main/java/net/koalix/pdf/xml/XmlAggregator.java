package net.koalix.pdf.xml;

import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.UserExtensionDto;
import net.koalix.pdf.xml.builders.CommercialDocumentXmlBuilder;
import net.koalix.pdf.xml.builders.UserExtensionXmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamWriter;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * Glue that assembles the final XML input to Apache FOP.
 *
 * <p>The shape is a single {@code <koalixcrm-export>} root element that
 * contains the document + the issuing user's extension. The XSL templates
 * pick nodes out of this tree via XPath.
 */
@Component
public class XmlAggregator {

    private final XMLOutputFactory outputFactory = XMLOutputFactory.newInstance();

    private final CommercialDocumentXmlBuilder documentBuilder;
    private final UserExtensionXmlBuilder userExtensionBuilder;

    public XmlAggregator(CommercialDocumentXmlBuilder documentBuilder,
                         UserExtensionXmlBuilder userExtensionBuilder) {
        this.documentBuilder = documentBuilder;
        this.userExtensionBuilder = userExtensionBuilder;
    }

    public byte[] build(CommercialDocumentDto document, UserExtensionDto userExtension)
            throws IOException {
        try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            XMLStreamWriter writer = outputFactory.createXMLStreamWriter(out, "UTF-8");
            try {
                writer.writeStartDocument("UTF-8", "1.0");
                writer.writeStartElement("koalixcrm-export");
                documentBuilder.write(writer, document);
                if (userExtension != null) {
                    userExtensionBuilder.write(writer, userExtension);
                }
                writer.writeEndElement();
                writer.writeEndDocument();
            } finally {
                writer.close();
            }
            return out.toByteArray();
        } catch (javax.xml.stream.XMLStreamException e) {
            throw new IOException("XML aggregation failed", e);
        }
    }
}
