package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

/**
 * Flat postal address as emitted inside a {@link NestedPartyDto} and inside a
 * {@link UserExtensionDto}. Purpose and validity are carried alongside the
 * address fields (the Python side reads an AddressAssignment joined to an
 * Address and projects the fields together).
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record NestedPostalAddressDto(
        Long id,
        String purpose,
        Boolean isPrimary,
        LocalDate validFrom,
        LocalDate validTo,
        String addressLine1,
        String addressLine2,
        String addressLine3,
        String addressLine4,
        String zipCode,
        String town,
        String state,
        String country,
        String subdivisionCode
) {}
