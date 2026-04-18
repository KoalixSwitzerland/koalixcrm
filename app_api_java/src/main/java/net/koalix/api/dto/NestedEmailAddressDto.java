package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record NestedEmailAddressDto(
        String purpose,
        Boolean isPrimary,
        String email
) {}
