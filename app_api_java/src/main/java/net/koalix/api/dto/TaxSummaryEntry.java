package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record TaxSummaryEntry(String rate, String taxableAmount, String taxAmount) {
}
