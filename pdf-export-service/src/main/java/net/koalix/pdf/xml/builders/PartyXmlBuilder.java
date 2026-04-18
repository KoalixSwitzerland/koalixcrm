package net.koalix.pdf.xml.builders;

import net.koalix.api.dto.NestedEmailAddressDto;
import net.koalix.api.dto.NestedPartyDto;
import net.koalix.api.dto.NestedPhoneNumberDto;
import net.koalix.api.dto.NestedPostalAddressDto;
import net.koalix.pdf.xml.XmlBuilder;
import org.springframework.stereotype.Component;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import static net.koalix.pdf.xml.XmlWriteSupport.writeAttribute;
import static net.koalix.pdf.xml.XmlWriteSupport.writeText;

/**
 * Emits a {@code <party>} element from a {@link NestedPartyDto}.
 *
 * <p>The XSL-FO templates switch on {@code @type} ({@code organization}
 * or {@code contact}) to pick the right name block — organizations render
 * {@code legal_name} + {@code legal_form}, natural-person contacts render
 * {@code prefix}/{@code given_name}/{@code family_name}. Postal, phone
 * and email blocks are ordered exactly as the backend emitted them;
 * {@code purpose} on each block is the purpose enum from the
 * AddressAssignment / PhoneAssignment / EmailAssignment row (billing,
 * shipping, legal, …).
 *
 * <p>Replaces the pre-v2.0.0 {@code ContactXmlBuilder} / {@code <contact>}
 * element. User XSL-FO templates that referenced {@code <contact>} need
 * to be updated to match — see
 * {@code docs/migration-v1.14.0-to-v2.0.0.md}.
 */
@Component
public class PartyXmlBuilder implements XmlBuilder<NestedPartyDto> {

    @Override
    public void write(XMLStreamWriter writer, NestedPartyDto dto) throws XMLStreamException {
        writer.writeStartElement("party");
        writeAttribute(writer, "id", dto.id());
        writeAttribute(writer, "type", dto.type());
        writeText(writer, "display_name", dto.displayName());

        if (dto.organization() != null) {
            NestedPartyDto.NestedOrganizationBlock org = dto.organization();
            writer.writeStartElement("organization");
            writeText(writer, "legal_name", org.legalName());
            writeText(writer, "legal_form", org.legalForm());
            writeText(writer, "registration_number", org.registrationNumber());
            writeText(writer, "legal_seat_country", org.legalSeatCountry());
            writer.writeEndElement();
        }
        if (dto.contact() != null) {
            NestedPartyDto.NestedContactBlock contact = dto.contact();
            writer.writeStartElement("contact");
            writeText(writer, "prefix", contact.prefix());
            writeText(writer, "given_name", contact.givenName());
            writeText(writer, "family_name", contact.familyName());
            writer.writeEndElement();
        }

        if (dto.postalAddresses() != null) {
            for (NestedPostalAddressDto addr : dto.postalAddresses()) {
                writePostal(writer, addr);
            }
        }
        if (dto.phoneNumbers() != null) {
            for (NestedPhoneNumberDto phone : dto.phoneNumbers()) {
                writePhone(writer, phone);
            }
        }
        if (dto.emailAddresses() != null) {
            for (NestedEmailAddressDto email : dto.emailAddresses()) {
                writeEmail(writer, email);
            }
        }
        writer.writeEndElement();
    }

    private void writePostal(XMLStreamWriter writer, NestedPostalAddressDto addr) throws XMLStreamException {
        writer.writeStartElement("postal_address");
        writeAttribute(writer, "purpose", addr.purpose());
        writeAttribute(writer, "is_primary", addr.isPrimary());
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

    private void writePhone(XMLStreamWriter writer, NestedPhoneNumberDto phone) throws XMLStreamException {
        writer.writeStartElement("phone_number");
        writeAttribute(writer, "purpose", phone.purpose());
        writeAttribute(writer, "is_primary", phone.isPrimary());
        writer.writeCharacters(phone.phoneE164() == null ? "" : phone.phoneE164());
        writer.writeEndElement();
    }

    private void writeEmail(XMLStreamWriter writer, NestedEmailAddressDto email) throws XMLStreamException {
        writer.writeStartElement("email_address");
        writeAttribute(writer, "purpose", email.purpose());
        writeAttribute(writer, "is_primary", email.isPrimary());
        writer.writeCharacters(email.email() == null ? "" : email.email());
        writer.writeEndElement();
    }
}
