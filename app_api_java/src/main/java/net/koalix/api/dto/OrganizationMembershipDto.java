package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record OrganizationMembershipDto(
        Long id,
        Long contact,
        Long organization,
        String title,
        String position,
        Boolean isPrimary,
        LocalDate validFrom,
        LocalDate validTo
) {
}
