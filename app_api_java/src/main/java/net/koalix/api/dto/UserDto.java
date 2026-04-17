package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record UserDto(Long id, String username, String firstName, String lastName, String email) {
}
