package net.koalix.pdf.config;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.SerializationFeature;
import net.koalix.api.CrmApiClient;
import net.koalix.api.OidcTokenProvider;
import org.apache.fop.apps.FopFactory;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.http.codec.json.Jackson2JsonEncoder;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.File;

@Configuration
@EnableConfigurationProperties(AppProperties.class)
public class Beans {

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
                .registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
                .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE)
                .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }

    @Bean
    public WebClient webClient(ObjectMapper objectMapper) {
        ExchangeStrategies strategies = ExchangeStrategies.builder()
                .codecs(cfg -> {
                    cfg.defaultCodecs().jackson2JsonEncoder(
                            new Jackson2JsonEncoder(objectMapper, MediaType.APPLICATION_JSON));
                    cfg.defaultCodecs().jackson2JsonDecoder(
                            new Jackson2JsonDecoder(objectMapper, MediaType.APPLICATION_JSON));
                })
                .build();
        return WebClient.builder().exchangeStrategies(strategies).build();
    }

    @Bean
    public OidcTokenProvider oidcTokenProvider(AppProperties props, WebClient webClient,
                                               ObjectMapper objectMapper) {
        var oidc = props.oidc();
        return new OidcTokenProvider(
                oidc.issuer(), oidc.clientId(), oidc.clientSecret(), oidc.scope(),
                webClient, objectMapper);
    }

    @Bean
    public CrmApiClient crmApiClient(AppProperties props, WebClient webClient,
                                     OidcTokenProvider tokens) {
        var origin = props.origin();
        String headerName = origin != null && origin.enabled() ? origin.headerName() : null;
        String headerValue = origin != null && origin.enabled() ? origin.headerValue() : null;
        return new CrmApiClient(webClient, tokens, props.crm().baseUrl(), headerName, headerValue);
    }

    @Bean
    public FopFactory fopFactory() {
        return FopFactory.newInstance(new File(".").toURI());
    }
}
