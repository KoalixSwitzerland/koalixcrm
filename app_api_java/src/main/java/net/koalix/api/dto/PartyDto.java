package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.OffsetDateTime;

/**
 * Party-pattern common supertype (issue #394). Mirrors the Django
 * {@code contacts.Party} REST shape served by {@code /parties/}.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyDto(
        Long id,
        String displayName,
        String defaultLanguage,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt,
        Long lastModifiedBy
) {
}
