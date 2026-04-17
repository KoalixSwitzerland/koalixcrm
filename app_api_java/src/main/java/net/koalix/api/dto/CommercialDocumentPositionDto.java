package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.math.BigDecimal;
import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record CommercialDocumentPositionDto(
        Long id,
        Integer positionNumber,
        String description,
        BigDecimal quantity,
        UnitDto unit,
        ProductTypeDto productType,
        BigDecimal discount,
        BigDecimal positionPricePerUnit,
        LocalDate lastPricingDate,
        BigDecimal lastCalculatedPrice,
        BigDecimal lastCalculatedTax,
        Boolean overwriteProductPrice
) {
}
