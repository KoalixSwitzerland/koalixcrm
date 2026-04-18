package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Standalone email address (issue #394).
 *
 * <p>Named {@code PartyEmailDto} for the duration of the transitional
 * naming window on the Python side. Will be renamed to
 * {@code EmailAddressDto} together with the Django class rename in the
 * G4 follow-up.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyEmailDto(Long id, String email) {
}
