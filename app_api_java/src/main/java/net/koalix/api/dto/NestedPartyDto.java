package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.List;

/**
 * Deeply-nested Party shape emitted by the
 * {@code /invoices/<id>/nested/} / {@code /quotations/<id>/nested/} etc.
 * endpoints — the input the PDF worker's XSL-FO templates consume.
 *
 * <p>Replaces the legacy {@code ContactDto} (dropped in v2.0.0). The
 * {@code type} field ("organization" / "contact") tells the XmlBuilder
 * which block to render; the other nested blocks ({@code organization},
 * {@code contact}) carry subclass-specific fields. Postal / phone /
 * email assignments are flat lists with purpose + validity baked onto
 * each row (no more MTI-style satellite tables).
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record NestedPartyDto(
        Long id,
        String displayName,
        String type,
        NestedOrganizationBlock organization,
        NestedContactBlock contact,
        List<NestedPostalAddressDto> postalAddresses,
        List<NestedPhoneNumberDto> phoneNumbers,
        List<NestedEmailAddressDto> emailAddresses
) {

    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record NestedOrganizationBlock(
            String legalName,
            String legalForm,
            String registrationNumber,
            String legalSeatCountry
    ) {}

    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record NestedContactBlock(
            String prefix,
            String givenName,
            String familyName
    ) {}
}
