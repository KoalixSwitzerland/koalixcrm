package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record ContactDto(
        Long id,
        String name,
        List<PostalAddressDto> postalAddresses,
        List<PhoneAddressDto> phoneAddresses,
        List<EmailAddressDto> emailAddresses
) {
}
