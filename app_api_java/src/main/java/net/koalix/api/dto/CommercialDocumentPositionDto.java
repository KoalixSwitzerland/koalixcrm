package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.math.BigDecimal;
import java.time.LocalDate;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public record CommercialDocumentPositionDto(
        Long id,
        Integer positionNumber,
        String description,
        BigDecimal quantity,
        UnitDto unit,
        ProductTypeDto productType,
        BigDecimal discount,
        BigDecimal positionPricePerUnit,
        BigDecimal positionTaxRate,
        LocalDate lastPricingDate,
        BigDecimal lastCalculatedPrice,
        BigDecimal lastCalculatedTax,
        Boolean overwriteProductPrice
) {
}
