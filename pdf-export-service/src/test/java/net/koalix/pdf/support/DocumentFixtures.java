package net.koalix.pdf.support;

import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.CommercialDocumentPositionDto;
import net.koalix.api.dto.ContactDto;
import net.koalix.api.dto.CurrencyDto;
import net.koalix.api.dto.PostalAddressDto;
import net.koalix.api.dto.ProductTypeDto;
import net.koalix.api.dto.TaxSummaryEntry;
import net.koalix.api.dto.UserDto;
import net.koalix.api.dto.UserExtensionDto;

import java.math.BigDecimal;
import java.util.List;

/**
 * Canonical DTO fixtures for integration tests. Minimal but non-null for
 * every required field so XML aggregation + XSL transform have something to
 * traverse.
 *
 * <p>Keep these in sync with the DTO records in {@code app_api_java} —
 * a record ctor change will surface here at compile time.
 */
public final class DocumentFixtures {

    private DocumentFixtures() {}

    public static CommercialDocumentDto invoice() {
        return new CommercialDocumentDto(
                17L, "Invoice", 12L,
                new ContactDto(
                        42L, "ACME SA",
                        List.of(new PostalAddressDto(
                                1L, "billing", null, null, "ACME SA",
                                "Bahnhofstrasse 1", null, null, null,
                                8001, "Zurich", null, "CH", null)),
                        List.of(), List.of()),
                null,
                5L,
                new CurrencyDto(1L, "Swiss Franc", "CHF", new BigDecimal("0.05")),
                "EXT-1", "Integration test invoice",
                BigDecimal.ZERO, null,
                new BigDecimal("1200.00"), new BigDecimal("97.20"),
                null, null, null, 3L,
                List.of(new CommercialDocumentPositionDto(
                        201L, 10, "Consulting hour", new BigDecimal("10.00"),
                        null,
                        new ProductTypeDto(301L, "CONS-H", "Consulting hour", null, null, null, "8.1"),
                        BigDecimal.ZERO, new BigDecimal("120.00"),
                        null,
                        new BigDecimal("1200.00"), new BigDecimal("97.20"),
                        Boolean.FALSE)),
                List.of(new TaxSummaryEntry("8.1", "1200.00", "97.20")),
                7L, null);
    }

    public static UserExtensionDto userExtension() {
        return new UserExtensionDto(
                7L,
                new UserDto(5L, "a.riedener", "Aaron", "Riedener", "a@example.com"),
                3L,
                new CurrencyDto(1L, null, "CHF", null),
                List.of(), List.of(), List.of());
    }
}
