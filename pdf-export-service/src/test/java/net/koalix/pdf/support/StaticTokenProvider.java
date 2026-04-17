package net.koalix.pdf.support;

import com.fasterxml.jackson.databind.ObjectMapper;
import net.koalix.api.OidcTokenProvider;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * Test-only stand-in for {@link OidcTokenProvider} that skips OIDC discovery
 * entirely and returns a constant token. Lets us drive {@code CrmApiClient}
 * without standing up an OIDC issuer in the integration tests.
 */
public class StaticTokenProvider extends OidcTokenProvider {

    private final String token;

    public StaticTokenProvider(String token) {
        super("https://invalid.test/issuer", "client", "secret", "scope",
                WebClient.builder().build(), new ObjectMapper());
        this.token = token;
    }

    @Override
    public String accessToken() {
        return token;
    }

    @Override
    public String refresh() {
        return token;
    }
}
