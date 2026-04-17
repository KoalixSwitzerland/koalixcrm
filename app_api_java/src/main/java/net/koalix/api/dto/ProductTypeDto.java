package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record ProductTypeDto(
        Long id,
        String productTypeIdentifier,
        String title,
        String description,
        UnitDto defaultUnit,
        TaxDto tax,
        String taxRate
) {
}
