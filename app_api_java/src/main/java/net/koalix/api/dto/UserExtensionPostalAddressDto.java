package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * Postal address attached to a UserExtension (the issuing user / company
 * block on rendered PDFs). Mirrors the Python
 * {@code UserExtensionPostalAddressSerializer} shape from
 * {@code djangoUserExtension.serializers.user_extension_nested}.
 *
 * <p>This is NOT the Party-pattern address shape — it's the legacy
 * concrete-table-inheritance satellite ({@code UserExtensionPostalAddress})
 * preserved for the user-extension "issuing company" data. Will be merged
 * onto the Party {@link AddressDto} / {@link NestedPostalAddressDto} flow
 * in the follow-up issue tracking the UserExtension satellite restructure.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record UserExtensionPostalAddressDto(
        Long id,
        String purpose,
        String prefix,
        String preName,
        String name,
        String addressLine1,
        String addressLine2,
        String addressLine3,
        String addressLine4,
        Integer zipCode,
        String town,
        String state,
        String country,
        String subdivisionCode
) {}
