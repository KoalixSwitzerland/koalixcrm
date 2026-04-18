package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.UserExtensionDto;
import net.koalix.api.dto.UserExtensionEmailAddressDto;
import net.koalix.api.dto.UserExtensionPhoneAddressDto;
import net.koalix.api.dto.UserExtensionPostalAddressDto;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

/**
 * Writes the issuing user / company block: the admin's UserExtension
 * aggregate is the XSL-FO template's source of truth for the company name,
 * address, logo contact info, and default currency.
 *
 * <p>Post-v2.0.0 the Party-pattern models took over "contact" data, but
 * the UserExtension satellites stayed on concrete-table inheritance.
 * See the follow-up issue on the UserExtension satellite restructure;
 * this builder works against the still-legacy shape.
 */
@Component
public class UserExtensionXmlBuilder implements XmlBuilder<UserExtensionDto> {

    @Override
    public void write(XMLStreamWriter writer, UserExtensionDto dto) throws XMLStreamException {
        writer.writeStartElement("user_extension");
        writeAttribute(writer, "id", dto.id());

        if (dto.user() != null) {
            writer.writeStartElement("user");
            writeAttribute(writer, "id", dto.user().id());
            writeText(writer, "username", dto.user().username());
            writeText(writer, "first_name", dto.user().firstName());
            writeText(writer, "last_name", dto.user().lastName());
            writeText(writer, "email", dto.user().email());
            writer.writeEndElement();
        }
        writeText(writer, "default_template_set", dto.defaultTemplateSet());
        if (dto.defaultCurrency() != null) {
            writer.writeStartElement("default_currency");
            writeAttribute(writer, "id", dto.defaultCurrency().id());
            writeText(writer, "short_name", dto.defaultCurrency().shortName());
            writer.writeEndElement();
        }
        if (dto.postalAddresses() != null) {
            for (UserExtensionPostalAddressDto addr : dto.postalAddresses()) {
                writer.writeStartElement("postal_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writeText(writer, "prefix", addr.prefix());
                writeText(writer, "pre_name", addr.preName());
                writeText(writer, "name", addr.name());
                writeText(writer, "address_line_1", addr.addressLine1());
                writeText(writer, "address_line_2", addr.addressLine2());
                writeText(writer, "zip_code", addr.zipCode());
                writeText(writer, "town", addr.town());
                writeText(writer, "country", addr.country());
                writer.writeEndElement();
            }
        }
        if (dto.phoneAddresses() != null) {
            for (UserExtensionPhoneAddressDto addr : dto.phoneAddresses()) {
                writer.writeStartElement("phone_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writer.writeCharacters(addr.phone() == null ? "" : addr.phone());
                writer.writeEndElement();
            }
        }
        if (dto.emailAddresses() != null) {
            for (UserExtensionEmailAddressDto addr : dto.emailAddresses()) {
                writer.writeStartElement("email_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writer.writeCharacters(addr.email() == null ? "" : addr.email());
                writer.writeEndElement();
            }
        }
        writer.writeEndElement();
    }
}
