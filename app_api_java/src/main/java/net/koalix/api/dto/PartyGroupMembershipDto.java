package net.koalix.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record PartyGroupMembershipDto(Long id, Long party, Long partyGroup) {
}
