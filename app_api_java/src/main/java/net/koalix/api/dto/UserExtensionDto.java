package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record UserExtensionDto(
        Long id,
        UserDto user,
        Long defaultTemplateSet,
        CurrencyDto defaultCurrency,
        List<NestedPostalAddressDto> postalAddresses,
        List<NestedPhoneAssignmentDto> phoneAddresses,
        List<NestedEmailAssignmentDto> emailAddresses
) {
}
