package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyRoleDto(
        Long id,
        Long party,
        String roleType,
        Boolean isPrimary,
        LocalDate validFrom,
        LocalDate validTo
) {
}
