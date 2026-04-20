package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.NestedEmailAssignmentDto;
import net.koalix.api.dto.NestedPhoneAssignmentDto;
import net.koalix.api.dto.NestedPostalAddressDto;
import net.koalix.api.dto.UserExtensionDto;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

/**
 * Writes the issuing user / company block: the admin's UserExtension
 * aggregate is the XSL-FO template's source of truth for the company name,
 * address, contact info, and default currency.
 *
 * <p>Emits the Party-pattern assignment-flattened shape, post-#396.
 * User XSL-FO templates that referenced the pre-v2.0.0 shape need to be
 * updated — see {@code docs/migration-v1.14.0-to-v2.0.0.md}.
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
            for (NestedPostalAddressDto addr : dto.postalAddresses()) {
                writer.writeStartElement("postal_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writeAttribute(writer, "is_primary", addr.isPrimary());
                writeText(writer, "valid_from", addr.validFrom() != null ? addr.validFrom().toString() : null);
                writeText(writer, "valid_to", addr.validTo() != null ? addr.validTo().toString() : null);
                writeText(writer, "address_line_1", addr.addressLine1());
                writeText(writer, "address_line_2", addr.addressLine2());
                writeText(writer, "address_line_3", addr.addressLine3());
                writeText(writer, "address_line_4", addr.addressLine4());
                writeText(writer, "zip_code", addr.zipCode());
                writeText(writer, "town", addr.town());
                writeText(writer, "state", addr.state());
                writeText(writer, "country", addr.country());
                writeText(writer, "subdivision_code", addr.subdivisionCode());
                writer.writeEndElement();
            }
        }
        if (dto.phoneAddresses() != null) {
            for (NestedPhoneAssignmentDto addr : dto.phoneAddresses()) {
                writer.writeStartElement("phone_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writeAttribute(writer, "is_primary", addr.isPrimary());
                writer.writeCharacters(addr.phoneE164() == null ? "" : addr.phoneE164());
                writer.writeEndElement();
            }
        }
        if (dto.emailAddresses() != null) {
            for (NestedEmailAssignmentDto addr : dto.emailAddresses()) {
                writer.writeStartElement("email_address");
                writeAttribute(writer, "purpose", addr.purpose());
                writeAttribute(writer, "is_primary", addr.isPrimary());
                writer.writeCharacters(addr.emailAddress() == null ? "" : addr.emailAddress());
                writer.writeEndElement();
            }
        }
        writer.writeEndElement();
    }
}
