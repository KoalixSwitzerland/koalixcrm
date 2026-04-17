package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record PostalAddressDto(
        Long id,
        String purpose,
        String prefix,
        String preName,
        String name,
        String addressLine1,
        String addressLine2,
        String addressLine3,
        String addressLine4,
        Integer zipCode,
        String town,
        String state,
        String country,
        String subdivisionCode
) {
}
