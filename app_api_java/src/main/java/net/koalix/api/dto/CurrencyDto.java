package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.math.BigDecimal;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record CurrencyDto(Long id, String description, String shortName, BigDecimal rounding) {
}
