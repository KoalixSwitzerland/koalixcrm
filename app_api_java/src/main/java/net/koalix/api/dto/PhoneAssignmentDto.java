package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record PhoneAssignmentDto(
        Long id,
        Long party,
        Long phone,
        String purpose,
        Boolean isPrimary,
        LocalDate validFrom,
        LocalDate validTo
) {
}
