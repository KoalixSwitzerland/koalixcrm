package net.koalix.pdf.xml;

import net.koalix.api.dto.CommercialDocumentDto;
import net.koalix.api.dto.CommercialDocumentPositionDto;
import net.koalix.api.dto.CurrencyDto;
import net.koalix.api.dto.NestedPartyDto;
import net.koalix.api.dto.NestedPartyDto.NestedOrganizationBlock;
import net.koalix.api.dto.ProductTypeDto;
import net.koalix.api.dto.TaxSummaryEntry;
import net.koalix.api.dto.UserDto;
import net.koalix.api.dto.UserExtensionDto;
import net.koalix.pdf.xml.builders.CommercialDocumentXmlBuilder;
import net.koalix.pdf.xml.builders.PartyXmlBuilder;
import net.koalix.pdf.xml.builders.PositionXmlBuilder;
import net.koalix.pdf.xml.builders.UserExtensionXmlBuilder;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class XmlAggregatorTest {

    @Test
    void buildsWellFormedRoot_withDocumentAndUserExtension() throws Exception {
        PartyXmlBuilder party = new PartyXmlBuilder();
        PositionXmlBuilder position = new PositionXmlBuilder();
        CommercialDocumentXmlBuilder docBuilder = new CommercialDocumentXmlBuilder(party, position);
        UserExtensionXmlBuilder ueBuilder = new UserExtensionXmlBuilder();
        XmlAggregator aggregator = new XmlAggregator(docBuilder, ueBuilder);

        CommercialDocumentDto document = new CommercialDocumentDto(
                17L, "Invoice", 12L,
                new NestedPartyDto(
                        42L, "ACME SA", "organization",
                        new NestedOrganizationBlock("ACME SA", "ag", null, "CH"),
                        null,
                        List.of(), List.of(), List.of()),
                5L,
                new CurrencyDto(1L, "Swiss Franc", "CHF", new BigDecimal("0.05")),
                "EXT-1", "Test invoice",
                BigDecimal.ZERO, null, new BigDecimal("1200.00"), new BigDecimal("97.20"),
                null, null, null, 3L,
                List.of(new CommercialDocumentPositionDto(
                        201L, 10, "Consulting hour", new BigDecimal("10.00"),
                        null,
                        new ProductTypeDto(301L, "CONS-H", "Consulting hour", null, null, null, "8.1"),
                        BigDecimal.ZERO, new BigDecimal("120.00"),
                        null, new BigDecimal("1200.00"), new BigDecimal("97.20"), Boolean.FALSE)),
                List.of(new TaxSummaryEntry("8.1", "1200.00", "97.20")),
                7L, null);

        UserExtensionDto userExtension = new UserExtensionDto(
                7L,
                new UserDto(5L, "a.riedener", "Aaron", "Riedener", "a@example.com"),
                3L, new CurrencyDto(1L, null, "CHF", null),
                List.of(), List.of(), List.of());

        byte[] xml = aggregator.build(document, userExtension);
        String s = new String(xml, java.nio.charset.StandardCharsets.UTF_8);
        assertThat(s).startsWith("<?xml");
        assertThat(s).contains("<koalixcrm-export>");
        assertThat(s).contains("<commercial_document type=\"Invoice\"");
        assertThat(s).contains("<party id=\"42\" type=\"organization\">");
        assertThat(s).contains("<user_extension id=\"7\">");
        assertThat(s).contains("<tax_summary>");
        assertThat(s).contains("<tax_bucket rate=\"8.1\">");
    }
}
