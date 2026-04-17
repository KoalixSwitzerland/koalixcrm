package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.CommercialDocumentPositionDto;
import net.koalix.api.dto.TaxSummaryEntry;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.util.Map;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

/**
 * Top-level builder for a {@link CommercialDocumentDto}.
 *
 * <p>Emits a {@code <commercial_document type="Invoice">} element with
 * all nested sub-blocks (customer/supplier contact, currency, positions,
 * tax summary, subclass-specific fields). The XSL-FO templates switch on
 * the {@code type} attribute to render each document kind.
 */
@Component
public class CommercialDocumentXmlBuilder implements XmlBuilder<CommercialDocumentDto> {

    private final ContactXmlBuilder contactBuilder;
    private final PositionXmlBuilder positionBuilder;

    public CommercialDocumentXmlBuilder(ContactXmlBuilder contactBuilder,
                                        PositionXmlBuilder positionBuilder) {
        this.contactBuilder = contactBuilder;
        this.positionBuilder = positionBuilder;
    }

    @Override
    public void write(XMLStreamWriter writer, CommercialDocumentDto dto) throws XMLStreamException {
        writer.writeStartElement("commercial_document");
        writeAttribute(writer, "type", dto.type());
        writeAttribute(writer, "id", dto.id());
        writeText(writer, "contract", dto.contract());
        writeText(writer, "staff", dto.staff());
        writeText(writer, "template_set", dto.templateSet());
        writeText(writer, "external_reference", dto.externalReference());
        writeText(writer, "description", dto.description());
        writeText(writer, "discount", dto.discount());
        writeText(writer, "last_pricing_date", dto.lastPricingDate());
        writeText(writer, "last_calculated_price", dto.lastCalculatedPrice());
        writeText(writer, "last_calculated_tax", dto.lastCalculatedTax());
        writeText(writer, "date_of_creation", dto.dateOfCreation());
        writeText(writer, "last_modification", dto.lastModification());
        writeText(writer, "custom_date_field", dto.customDateField());

        if (dto.currency() != null) {
            writer.writeStartElement("currency");
            writeAttribute(writer, "id", dto.currency().id());
            writeText(writer, "short_name", dto.currency().shortName());
            writeText(writer, "description", dto.currency().description());
            writer.writeEndElement();
        }
        if (dto.customer() != null) {
            writer.writeStartElement("customer");
            contactBuilder.write(writer, dto.customer());
            writer.writeEndElement();
        }
        if (dto.supplier() != null) {
            writer.writeStartElement("supplier");
            contactBuilder.write(writer, dto.supplier());
            writer.writeEndElement();
        }
        if (dto.items() != null) {
            writer.writeStartElement("items");
            for (CommercialDocumentPositionDto p : dto.items()) {
                positionBuilder.write(writer, p);
            }
            writer.writeEndElement();
        }
        if (dto.taxSummary() != null) {
            writer.writeStartElement("tax_summary");
            for (TaxSummaryEntry entry : dto.taxSummary()) {
                writer.writeStartElement("tax_bucket");
                writeAttribute(writer, "rate", entry.rate());
                writeText(writer, "taxable_amount", entry.taxableAmount());
                writeText(writer, "tax_amount", entry.taxAmount());
                writer.writeEndElement();
            }
            writer.writeEndElement();
        }
        if (dto.extra() != null) {
            writer.writeStartElement("extra");
            for (Map.Entry<String, Object> e : dto.extra().entrySet()) {
                writeText(writer, e.getKey(), e.getValue());
            }
            writer.writeEndElement();
        }
        writer.writeEndElement();
    }
}
