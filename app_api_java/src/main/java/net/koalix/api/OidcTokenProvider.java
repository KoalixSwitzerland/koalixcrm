package net.koalix.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.atomic.AtomicReference;

/**
 * OIDC M2M client_credentials token provider with discovery + caching.
 *
 * <p>Discovers the token endpoint from
 * {@code ${issuer}/.well-known/openid-configuration} on first call, then
 * caches both the token endpoint and the access token until
 * {@code exp - 30 s}.
 *
 * <p>Thread-safe: the cached token is held in an {@link AtomicReference}.
 */
public class OidcTokenProvider {

    private static final Logger LOG = LoggerFactory.getLogger(OidcTokenProvider.class);
    private static final Duration TOKEN_SAFETY_MARGIN = Duration.ofSeconds(30);

    private final String issuer;
    private final String clientId;
    private final String clientSecret;
    private final String scope;
    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    private final AtomicReference<String> tokenEndpoint = new AtomicReference<>();
    private final AtomicReference<CachedToken> cached = new AtomicReference<>();

    public OidcTokenProvider(String issuer, String clientId, String clientSecret, String scope,
                             WebClient webClient, ObjectMapper objectMapper) {
        this.issuer = issuer;
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.scope = scope;
        this.webClient = webClient;
        this.objectMapper = objectMapper;
    }

    public String accessToken() {
        var current = cached.get();
        if (current != null && Instant.now().isBefore(current.expiresAt.minus(TOKEN_SAFETY_MARGIN))) {
            return current.accessToken;
        }
        return refresh();
    }

    public String refresh() {
        var ep = tokenEndpoint.get();
        if (ep == null) {
            ep = discoverTokenEndpoint();
            tokenEndpoint.set(ep);
        }
        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "client_credentials");
        form.add("client_id", clientId);
        form.add("client_secret", clientSecret);
        if (scope != null && !scope.isBlank()) {
            form.add("scope", scope);
        }
        JsonNode response = webClient.post()
                .uri(ep)
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .body(BodyInserters.fromFormData(form))
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block();
        if (response == null || !response.hasNonNull("access_token")) {
            throw new IllegalStateException("OIDC token endpoint returned no access_token");
        }
        int expiresIn = response.path("expires_in").asInt(300);
        String token = response.get("access_token").asText();
        Instant expiresAt = Instant.now().plusSeconds(expiresIn);
        cached.set(new CachedToken(token, expiresAt));
        LOG.debug("Refreshed OIDC token, expires at {}", expiresAt);
        return token;
    }

    private String discoverTokenEndpoint() {
        String url = issuer.replaceAll("/+$", "") + "/.well-known/openid-configuration";
        JsonNode doc = webClient.get()
                .uri(url)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .block();
        if (doc == null || !doc.hasNonNull("token_endpoint")) {
            throw new IllegalStateException("OIDC discovery document has no token_endpoint: " + url);
        }
        return doc.get("token_endpoint").asText();
    }

    private record CachedToken(String accessToken, Instant expiresAt) {
    }
}
