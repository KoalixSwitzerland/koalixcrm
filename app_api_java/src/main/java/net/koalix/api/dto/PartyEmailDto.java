package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Standalone email address (issue #394).
 *
 * <p>Named {@code PartyEmailDto} (not {@code EmailAddressDto}) for the
 * duration of the Party migration to avoid colliding with the legacy
 * {@link EmailAddressDto} (which carries a purpose field and a person FK
 * baked in). Renamed to {@code EmailAddressDto} in PR #395.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyEmailDto(Long id, String email) {
}
