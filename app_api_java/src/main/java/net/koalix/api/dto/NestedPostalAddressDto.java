package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Flat postal address as emitted inside a {@link NestedPartyDto}. Purpose
 * and validity are carried alongside the address fields (the Python
 * side is really reading an AddressAssignment joined to an Address and
 * projecting the fields together).
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record NestedPostalAddressDto(
        String purpose,
        Boolean isPrimary,
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
