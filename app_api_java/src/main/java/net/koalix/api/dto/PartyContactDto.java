package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;
import java.time.OffsetDateTime;

/**
 * Natural-person Party (UBL 2.3 "Contact"). Mirrors the Django
 * {@code contacts.PartyContact} REST shape served by {@code /party_contacts/}.
 *
 * <p>Named {@code PartyContactDto} for the duration of the transitional
 * naming window on the Python side. Will be renamed to {@code ContactDto}
 * together with the Django class rename in the G4 follow-up.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyContactDto(
        Long id,
        String displayName,
        String defaultLanguage,
        String prefix,
        String givenName,
        String familyName,
        LocalDate dateOfBirth,
        LocalDate gdprConsentDate,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
