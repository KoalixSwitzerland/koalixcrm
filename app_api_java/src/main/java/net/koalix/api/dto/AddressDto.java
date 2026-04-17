package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Standalone address (issue #394). Unlike the legacy {@link PostalAddressDto}
 * it has no purpose / person_name / person_prefix on the record itself —
 * purpose and validity live on the {@link AddressAssignmentDto}, and
 * person-like prefix/name fields live on {@link PartyContactDto}.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AddressDto(
        Long id,
        String addressLine1,
        String addressLine2,
        String addressLine3,
        String addressLine4,
        String zipCode,
        String town,
        String state,
        String country,
        String subdivisionCode
) {
}
