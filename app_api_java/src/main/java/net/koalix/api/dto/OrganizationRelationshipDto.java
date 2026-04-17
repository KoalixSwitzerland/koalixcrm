package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record OrganizationRelationshipDto(
        Long id,
        Long parent,
        Long child,
        String relationshipType,
        LocalDate validFrom,
        LocalDate validTo
) {
}
