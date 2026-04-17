package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.ContactDto;
import net.koalix.api.dto.EmailAddressDto;
import net.koalix.api.dto.PhoneAddressDto;
import net.koalix.api.dto.PostalAddressDto;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

@Component
public class ContactXmlBuilder implements XmlBuilder<ContactDto> {

    @Override
    public void write(XMLStreamWriter writer, ContactDto dto) throws XMLStreamException {
        writer.writeStartElement("contact");
        writeAttribute(writer, "id", dto.id());
        writeText(writer, "name", dto.name());

        if (dto.postalAddresses() != null) {
            for (PostalAddressDto addr : dto.postalAddresses()) {
                writePostal(writer, addr);
            }
        }
        if (dto.phoneAddresses() != null) {
            for (PhoneAddressDto addr : dto.phoneAddresses()) {
                writePhone(writer, addr);
            }
        }
        if (dto.emailAddresses() != null) {
            for (EmailAddressDto addr : dto.emailAddresses()) {
                writeEmail(writer, addr);
            }
        }
        writer.writeEndElement();
    }

    private void writePostal(XMLStreamWriter writer, PostalAddressDto addr) throws XMLStreamException {
        writer.writeStartElement("postal_address");
        writeAttribute(writer, "purpose", addr.purpose());
        writeText(writer, "prefix", addr.prefix());
        writeText(writer, "pre_name", addr.preName());
        writeText(writer, "name", addr.name());
        writeText(writer, "address_line_1", addr.addressLine1());
        writeText(writer, "address_line_2", addr.addressLine2());
        writeText(writer, "address_line_3", addr.addressLine3());
        writeText(writer, "address_line_4", addr.addressLine4());
        writeText(writer, "zip_code", addr.zipCode());
        writeText(writer, "town", addr.town());
        writeText(writer, "state", addr.state());
        writeText(writer, "country", addr.country());
        writer.writeEndElement();
    }

    private void writePhone(XMLStreamWriter writer, PhoneAddressDto addr) throws XMLStreamException {
        writer.writeStartElement("phone_address");
        writeAttribute(writer, "purpose", addr.purpose());
        writer.writeCharacters(addr.phone() == null ? "" : addr.phone());
        writer.writeEndElement();
    }

    private void writeEmail(XMLStreamWriter writer, EmailAddressDto addr) throws XMLStreamException {
        writer.writeStartElement("email_address");
        writeAttribute(writer, "purpose", addr.purpose());
        writer.writeCharacters(addr.email() == null ? "" : addr.email());
        writer.writeEndElement();
    }
}
