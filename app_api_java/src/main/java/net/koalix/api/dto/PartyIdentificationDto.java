package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyIdentificationDto(
        Long id,
        Long party,
        String scheme,
        String value,
        LocalDate validFrom,
        LocalDate validTo
) {
}
