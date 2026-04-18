package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.OffsetDateTime;

/**
 * Legal-person Party (AG, GmbH, Verein, …). Mirrors the Django
 * {@code contacts.Organization} REST shape served by {@code /organizations/}.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record OrganizationDto(
        Long id,
        String displayName,
        String defaultLanguage,
        String legalForm,
        String legalName,
        String registrationNumber,
        String legalSeatCountry,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
