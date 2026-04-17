package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDate;
import java.time.OffsetDateTime;

/**
 * Natural-person Party (UBL 2.3 "Contact"). Mirrors the Django
 * {@code contacts.PartyContact} REST shape served by {@code /party_contacts/}.
 *
 * <p>Named {@code PartyContactDto} (not {@code ContactDto}) for the duration of
 * the Party migration (PR #394) to avoid colliding with the legacy
 * {@link ContactDto}, which still represents the org-like entity embedded in
 * nested commercial-document responses. Renamed to {@code ContactDto} in PR
 * #395 once the legacy {@link ContactDto} is removed.
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
        String preferredLanguage,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
