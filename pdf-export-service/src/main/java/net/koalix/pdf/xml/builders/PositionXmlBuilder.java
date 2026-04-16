package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.CommercialDocumentPositionDto;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

@Component
public class PositionXmlBuilder implements XmlBuilder<CommercialDocumentPositionDto> {

    @Override
    public void write(XMLStreamWriter writer, CommercialDocumentPositionDto dto) throws XMLStreamException {
        writer.writeStartElement("position");
        writeAttribute(writer, "id", dto.id());
        writeText(writer, "position_number", dto.positionNumber());
        writeText(writer, "description", dto.description());
        writeText(writer, "quantity", dto.quantity());
        writeText(writer, "discount", dto.discount());
        writeText(writer, "position_price_per_unit", dto.positionPricePerUnit());
        writeText(writer, "last_calculated_price", dto.lastCalculatedPrice());
        writeText(writer, "last_calculated_tax", dto.lastCalculatedTax());

        if (dto.unit() != null) {
            writer.writeStartElement("unit");
            writeAttribute(writer, "id", dto.unit().id());
            writeText(writer, "description", dto.unit().description());
            writeText(writer, "short_name", dto.unit().shortName());
            writer.writeEndElement();
        }
        if (dto.productType() != null) {
            writer.writeStartElement("product_type");
            writeAttribute(writer, "id", dto.productType().id());
            writeText(writer, "title", dto.productType().title());
            writeText(writer, "product_type_identifier", dto.productType().productTypeIdentifier());
            writeText(writer, "description", dto.productType().description());
            writeText(writer, "tax_rate", dto.productType().taxRate());
            writer.writeEndElement();
        }
        writer.writeEndElement();
    }
}
