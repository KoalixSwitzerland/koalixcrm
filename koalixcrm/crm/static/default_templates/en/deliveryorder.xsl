<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
        xmlns:fo="http://www.w3.org/1999/XSL/Format">
    <xsl:decimal-format name="european" decimal-separator="," grouping-separator="."/>
    <xsl:template match="django-objects">
        <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
            <!-- defines page layout -->
            <fo:layout-master-set>
                <fo:simple-page-master master-name="simple"
                                       page-height="29.7cm"
                                       page-width="21cm"
                                       margin-top="1.5cm"
                                       margin-bottom="1.0cm"
                                       margin-left="1.5cm"
                                       margin-right="1.5cm">
                    <fo:region-body margin-top="3.0cm" margin-bottom="1.5cm"/>
                    <fo:region-before extent="4.5cm"/>
                    <fo:region-after extent="1.5cm"/>
                </fo:simple-page-master>
            </fo:layout-master-set>
            <fo:page-sequence master-reference="simple">
                <fo:static-content flow-name="xsl-region-before">
                    <fo:table table-layout="fixed" width="100%">
                        <fo:table-column column-width="15.2cm"/>
                        <fo:table-column column-width="2.8cm"/>
                        <fo:table-body font-size="9pt"
                                       font-family="BitstreamVeraSans">
                            <fo:table-row height="2cm" border-bottom-color="black" border-bottom-style="solid"
                                          border-bottom-width="0.5pt">
                                <fo:table-cell padding-bottom="3pt">
                                    <fo:block text-align="left">
                                        <fo:external-graphic content-width="6.0cm">
                                            <xsl:attribute name="src">
                                                file:///<xsl:value-of select="filebrowser_directory"/>/<xsl:value-of
                                                    select="object[@model='djangoUserExtension.documenttemplate']/field[@name='logo']"/>
                                            </xsl:attribute>
                                        </fo:external-graphic>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding-bottom="3pt">
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left"
                                              margin-top="0.15cm">Irgendeine Firma
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Irgendwostrasse 12
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">CH-8000 Zürich
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">www.koalix.org
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">emailaddress@gmail.com
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">+41 79 xxx xx xx
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                </fo:static-content>
                <fo:static-content flow-name="xsl-region-after">
                    <fo:block font-size="8pt"
                              font-family="BitstreamVeraSans"
                              text-align="left">
                        <xsl:text> </xsl:text>
                    </fo:block>
                    <fo:table table-layout="fixed" width="100%">
                        <fo:table-column column-width="5.0cm"/>
                        <fo:table-column column-width="5.0cm"/>
                        <fo:table-column column-width="5.0cm"/>
                        <fo:table-column column-width="3.0cm"/>
                        <fo:table-body>
                            <fo:table-row border-top-color="black" border-top-style="solid" border-top-width="0.5pt"
                                          height="0.1cm">
                                <fo:table-cell number-columns-spanned="4">
                                    <fo:block font-size="5pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left"
                                              font-weight="bold"
                                    >
                                        <xsl:text> </xsl:text>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="start">
                                        <xsl:value-of
                                                select="object[@model='djangoUserExtension.documenttemplate']/field[@name='pagefooterleft']"/>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="end">
                                        <xsl:value-of
                                                select="object[@model='djangoUserExtension.documenttemplate']/field[@name='pagefootermiddle']"/>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="end">
                                        <xsl:value-of
                                                select="object[@model='djangoUserExtension.documenttemplate']/field[@name='bankingaccountref']"/>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="end">Seite<fo:page-number/>/
                                        <fo:page-number-citation ref-id="last-page"/>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                </fo:static-content>
                <fo:flow flow-name="xsl-region-body">
                    <fo:table table-layout="fixed" width="100%" margin-top="1.0cm">
                        <fo:table-column column-width="3cm"/>
                        <fo:table-column column-width="7cm"/>
                        <fo:table-column column-width="8cm"/>
                        <fo:table-body font-size="7pt"
                                       font-family="BitstreamVeraSans">
                            <fo:table-row>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Kundennummer
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Projektnummer
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Liferscheinnummer
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Bankverbindung
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">CHF Konto IBAN
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">EUR Konto IBAN
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">SWIFT Adresse
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">MwSt Nummer
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Erstellt am
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Zahlbar bis
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Verantwortlich
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Phone direkt
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">E-mail direkt
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Ihre Referenz
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">KUN-<xsl:value-of
                                            select="object[@model='crm.contact']/@pk"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">PRO-<xsl:value-of
                                            select="object[@model='crm.salesdocument']/field[@name='contract']"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">LIF-<xsl:value-of
                                            select="object[@model='crm.salesdocument']/@pk"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Angaben zur Bank
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">IBAN des Kontos
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">Internationale IBAN des Kontos
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">ClearingNummer Der Bank
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">MwSt Nummer
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of
                                                select="substring(object[@model='crm.salesdocument']/field[@name='date_of_creation'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of
                                            select="substring(object[@model='crm.salesdocument']/field[@name='date_of_creation'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of
                                            select="substring(object[@model='crm.salesdocument']/field[@name='date_of_creation'], 1, 4)"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of
                                                select="substring(object[@model='crm.deliverynote']/field[@name='delivery_date'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of
                                            select="substring(object[@model='crm.deliverynote']/field[@name='delivery_date'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of
                                            select="substring(object[@model='crm.deliverynote']/field[@name='delivery_date'], 1, 4)"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of select="object[@model='auth.user']/field[@name='first_name']"/><xsl:text> </xsl:text>
                                        <xsl:value-of select="object[@model='auth.user']/field[@name='last_name']"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of select="object[@model='crm.phoneaddress']/field[@name='phone']"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of select="object[@model='auth.user']/field[@name='email']"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <fo:leader leader-pattern="space"/>
                                    </fo:block>
                                    <fo:block font-size="7pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of
                                                select="object[@model='crm.salesdocument']/field[@name='external_reference']"/>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block font-size="6pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left"
                                              text-decoration="underline"
                                              margin-bottom="0.5cm">
                                        <xsl:value-of
                                                select="object[@model='djangoUserExtension.templateset']/field[@name='addresser']"/>
                                    </fo:block>
                                    <fo:block font-size="9pt"
                                              font-family="BitstreamVeraSans"
                                              text-align="left">
                                        <xsl:value-of select="object[@model='crm.contact']/field[@name='name']"/>
                                    </fo:block>
                                    <xsl:choose>
                                        <xsl:when
                                                test="object[@model='crm.postaladdressforcontact']/field[@name='purpose']">
                                            <fo:block font-size="9pt"
                                                      font-family="BitstreamVeraSans"
                                                      text-align="left">
                                                <xsl:value-of
                                                        select="object[@model='crm.postaladdress']/field[@name='pre_name']"/><xsl:text> </xsl:text>
                                                <xsl:value-of
                                                        select="object[@model='crm.postaladdress']/field[@name='name']"/>
                                            </fo:block>
                                            <xsl:choose>
                                                <xsl:when
                                                        test="object[@model='crm.postaladdress']/field[@name='address_line_1']">
                                                    <fo:block font-size="9pt"
                                                              font-family="BitstreamVeraSans"
                                                              text-align="left">
                                                        <xsl:value-of
                                                                select="object[@model='crm.postaladdress']/field[@name='address_line_1']"/>
                                                    </fo:block>
                                                </xsl:when>
                                            </xsl:choose>
                                            <xsl:choose>
                                                <xsl:when
                                                        test="object[@model='crm.postaladdress']/field[@name='address_line_2']">
                                                    <fo:block font-size="9pt"
                                                              font-family="BitstreamVeraSans"
                                                              text-align="left">
                                                        <xsl:value-of
                                                                select="object[@model='crm.postaladdress']/field[@name='address_line_2']"/>
                                                    </fo:block>
                                                </xsl:when>
                                            </xsl:choose>
                                            <xsl:choose>
                                                <xsl:when
                                                        test="object[@model='crm.postaladdress']/field[@name='address_line_3']">
                                                    <fo:block font-size="9pt"
                                                              font-family="BitstreamVeraSans"
                                                              text-align="left">
                                                        <xsl:value-of
                                                                select="object[@model='crm.postaladdress']/field[@name='address_line_3']"/>
                                                    </fo:block>
                                                </xsl:when>
                                            </xsl:choose>
                                            <xsl:choose>
                                                <xsl:when
                                                        test="object[@model='crm.postaladdress']/field[@name='address_line_4']">
                                                    <fo:block font-size="9pt"
                                                              font-family="BitstreamVeraSans"
                                                              text-align="left">
                                                        <xsl:value-of
                                                                select="object[@model='crm.postaladdress']/field[@name='address_line_4']"/>
                                                    </fo:block>
                                                </xsl:when>
                                            </xsl:choose>
                                            <fo:block font-size="9pt"
                                                      font-family="BitstreamVeraSans"
                                                      text-align="left">
                                                <xsl:value-of
                                                        select="object[@model='crm.postaladdress']/field[@name='country']"/><xsl:text>-</xsl:text><xsl:value-of
                                                    select="object[@model='crm.postaladdress']/field[@name='zip_code']"/>
                                                <xsl:text> </xsl:text>
                                                <xsl:value-of
                                                        select="object[@model='crm.postaladdress']/field[@name='town']"/>
                                            </fo:block>
                                        </xsl:when>
                                    </xsl:choose>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                    <xsl:for-each select="object[@model='crm.textparagraphinsalesdocument']">
                        <xsl:choose>
                            <xsl:when test="field[@name='purpose']='BS'">
                                <fo:block font-size="9pt"
                                          font-family="BitstreamVeraSans"
                                          color="black"
                                          text-align="left"
                                          margin-top="2cm"
                                          linefeed-treatment="preserve">
                                    <xsl:value-of select="field[@name='text_paragraph']"/>
                                </fo:block>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:for-each>
                    <fo:block font-size="15pt"
                              font-family="BitstreamVeraSans"
                              color="black"
                              text-align="left"
                              font-weight="bold"
                              margin-top="2cm">
                        Delivery note
                        <xsl:value-of select="object[@model='crm.salesdocument']/field[@name='description']"/>
                    </fo:block>
                    <xsl:for-each select="object[@model='crm.textparagraphinsalesdocument']">
                        <xsl:choose>
                            <xsl:when test="field[@name='purpose']='AS'">
                                <fo:block font-size="9pt"
                                          font-family="BitstreamVeraSans"
                                          color="black"
                                          text-align="left"
                                          margin-top="2cm"
                                          linefeed-treatment="preserve"
                                          page-break-after="always">
                                    <xsl:value-of select="field[@name='text_paragraph']"/>
                                </fo:block>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:for-each>
                    <fo:block font-size="9pt"
                              font-family="BitstreamVeraSans"
                              text-align="left"
                              line-height="13pt">
                        <xsl:text> </xsl:text>
                    </fo:block>
                    <fo:table table-layout="fixed" width="100%">
                        <fo:table-column column-width="1.0cm"/>
                        <fo:table-column column-width="9.5cm"/>
                        <fo:table-column column-width="2.5cm"/>
                        <fo:table-column column-width="2.5cm"/>
                        <fo:table-column column-width="2.5cm"/>
                        <fo:table-header font-size="9pt"
                                         line-height="9pt"
                                         font-weight="bold"
                                         font-family="BitstreamVeraSans">
                            <fo:table-cell border-color="black"
                                           border-style="solid"
                                           border-width="0.5pt"
                                           padding="5.0pt">
                                <fo:block text-align="start">Pos.</fo:block>
                            </fo:table-cell>
                            <fo:table-cell border-color="black"
                                           border-style="solid"
                                           border-width="0.5pt"
                                           padding="5.0pt">
                                <fo:block text-align="start">Beschreibung</fo:block>
                            </fo:table-cell>
                            <fo:table-cell border-color="black"
                                           border-style="solid"
                                           border-width="0.5pt"
                                           padding="5.0pt">
                                <fo:block text-align="end">Anzahl</fo:block>
                            </fo:table-cell>
                            <fo:table-cell border-color="black"
                                           border-style="solid"
                                           border-width="0.5pt"
                                           padding="5.0pt">
                                <fo:block text-align="end">Einzelpreis</fo:block>
                            </fo:table-cell>
                            <fo:table-cell border-color="black"
                                           border-style="solid"
                                           border-width="0.5pt"
                                           padding="5.0pt">
                                <fo:block text-align="end">Summe</fo:block>
                            </fo:table-cell>
                        </fo:table-header>
                        <fo:table-body font-size="9pt"
                                       font-family="BitstreamVeraSans">
                            <xsl:for-each select="object[@model='crm.position']">
                                <xsl:sort select="field[@name=position_number]" data-type="number"/>
                                <fo:table-row keep-together.within-page="always">
                                    <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                                   padding="5.0pt">
                                        <fo:block text-align="start">
                                            <xsl:value-of select="field[@name='position_number']"/>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                                   padding="5.0pt">
                                        <xsl:variable name="product_in_this_position" select="field[@name='product']"/>
                                        <fo:block text-align="start"
                                                  font-weight="bold"
                                                  font-size="8pt"
                                                  font-family="BitstreamVeraSans"
                                                  line-height="9pt">
                                            <xsl:value-of
                                                    select="../object[@model='crm.product' and @pk=$product_in_this_position]/field[@name='title']"/>
                                        </fo:block>
                                        <xsl:choose>
                                            <xsl:when
                                                    test="../object[@model='crm.product' and @pk=$product_in_this_position]/field[@name='description']/None">
                                                <fo:block text-align="start"
                                                          font-size="7pt"
                                                          font-family="BitstreamVeraSans"
                                                          linefeed-treatment="preserve">
                                                    <xsl:value-of select="field[@name='description']"/>
                                                </fo:block>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <fo:block text-align="start"
                                                          font-size="7pt"
                                                          font-family="BitstreamVeraSans"
                                                          linefeed-treatment="preserve">
                                                    <xsl:value-of
                                                            select="../object[@model='crm.product' and @pk=$product_in_this_position]/field[@name='description']"/>
                                                </fo:block>
                                                <fo:block text-align="start"
                                                          font-size="7pt"
                                                          font-family="BitstreamVeraSans"
                                                          linefeed-treatment="preserve"
                                                          padding-top="0.1cm">
                                                    <xsl:value-of select="field[@name='description']"/>
                                                </fo:block>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </fo:table-cell>
                                    <fo:table-cell border-color="black"
                                                   border-style="solid"
                                                   border-width="0.5pt"
                                                   padding="5.0pt">
                                        <fo:block text-align="end"
                                                  font-size="8pt">
                                            <xsl:choose>
                                                <xsl:when test="field[@name='quantity'] = '0E-15'">-</xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of
                                                            select="format-number(field[@name='quantity'], '#.##0,00', 'european')"/>
                                                    <xsl:text> </xsl:text>
                                                    <xsl:variable name="unitinthisposition"
                                                                  select="field[@name='unit']"/>
                                                    <xsl:value-of
                                                            select="../object[@model='crm.unit' and @pk=$unitinthisposition]/field[@name='short_name']"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell border-color="black"
                                                   border-style="solid"
                                                   border-width="0.5pt"
                                                   padding="5.0pt">
                                        <fo:block text-align="end" font-size="8pt">
                                            <xsl:choose>
                                                <xsl:when test="field[@name='position_price_per_unit']/None">-
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of
                                                            select="format-number(field[@name='position_price_per_unit'], '#.##0,00', 'european')"/>
                                                    <xsl:text> </xsl:text>
                                                    <xsl:value-of
                                                            select="../object[@model='crm.currency']/field[@name='short_name']"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </fo:block>
                                    </fo:table-cell>
                                    <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                                   padding="5.0pt">
                                        <fo:block text-align="end" font-size="8pt">
                                            <xsl:choose>
                                                <xsl:when test="field[@name='last_calculated_price']/None">-</xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of
                                                            select="format-number(field[@name='last_calculated_price'], '#.##0,00', 'european')"/>
                                                    <xsl:text> </xsl:text>
                                                    <xsl:value-of
                                                            select="../object[@model='crm.currency']/field[@name='short_name']"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </fo:block>
                                    </fo:table-cell>
                                </fo:table-row>
                            </xsl:for-each>
                            <fo:table-row keep-together="always" keep-with-previous="always">
                                <fo:table-cell number-columns-spanned="5">
                                    <fo:block text-align="start" margin-top="0.5cm">
                                        <xsl:text> </xsl:text>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row keep-together="always" keep-with-previous="always">
                                <fo:table-cell number-columns-spanned="2">
                                    <fo:block text-align="start">
                                        <xsl:text> </xsl:text>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                               padding="5.0pt">
                                    <fo:block text-align="start">
                                        Subtotal
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell number-columns-spanned="2"
                                               border-color="black"
                                               border-style="solid"
                                               border-width="0.5pt"
                                               padding="5.0pt">
                                    <fo:block text-align="end" font-size="8pt">
                                        <xsl:choose>
                                            <xsl:when
                                                    test="object[@model='crm.salesdocument']/field[@name='last_calculated_price']/None">
                                                -
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of
                                                        select="format-number(object[@model='crm.salesdocument']/field[@name='last_calculated_price'], '#.##0,00', 'european')"/>
                                                <xsl:text> </xsl:text>
                                                <xsl:value-of
                                                        select="object[@model='crm.currency']/field[@name='short_name']"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <xsl:choose>
                                <xsl:when
                                        test="object[@model='crm.salesdocument']/field[@name='last_calculated_tax']!='0.00'">
                                    <fo:table-row keep-together="always" keep-with-previous="always">
                                        <fo:table-cell number-columns-spanned="2">
                                            <fo:block text-align="start"></fo:block>
                                        </fo:table-cell>
                                        <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                                       padding="5.0pt">
                                            <fo:block text-align="start">MwSt 8.0%</fo:block>
                                        </fo:table-cell>
                                        <fo:table-cell number-columns-spanned="2"
                                                       border-color="black"
                                                       border-style="solid"
                                                       border-width="0.5pt"
                                                       padding="5.0pt">
                                            <fo:block text-align="end" font-size="8pt">
                                                <xsl:value-of
                                                        select="format-number(object[@model='crm.salesdocument']/field[@name='last_calculated_tax'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:text> </xsl:text><xsl:value-of
                                                    select="object[@model='crm.currency']/field[@name='short_name']"/>
                                            </fo:block>
                                        </fo:table-cell>
                                    </fo:table-row>
                                </xsl:when>
                                <xsl:otherwise>
                                    <fo:table-row keep-together="always" keep-with-previous="always">
                                        <fo:table-cell number-columns-spanned="2">
                                            <fo:block text-align="start"></fo:block>
                                        </fo:table-cell>
                                        <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                                       padding="5.0pt">
                                            <fo:block text-align="start">exkl. MwSt</fo:block>
                                        </fo:table-cell>
                                        <fo:table-cell number-columns-spanned="2"
                                                       border-color="black"
                                                       border-style="solid"
                                                       border-width="0.5pt"
                                                       padding="5.0pt">
                                            <fo:block text-align="end" font-size="7pt"></fo:block>
                                        </fo:table-cell>
                                    </fo:table-row>
                                </xsl:otherwise>
                            </xsl:choose>
                            <fo:table-row keep-together="always" keep-with-previous="always">
                                <fo:table-cell number-columns-spanned="2">
                                    <fo:block text-align="start">
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt"
                                               padding="5.0pt">
                                    <fo:block text-align="start" font-weight="bold">
                                        Total
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell number-columns-spanned="2"
                                               border-color="black"
                                               border-style="solid"
                                               border-width="0.5pt"
                                               padding="5.0pt">
                                    <fo:block text-align="end" font-weight="bold" font-size="8pt">
                                        <xsl:choose>
                                            <xsl:when
                                                    test="object[@model='crm.salesdocument']/field[@name='last_calculated_price']/None">
                                                -
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of
                                                        select="format-number(object[@model='crm.salesdocument']/field[@name='last_calculated_price']+object[@model='crm.salesdocument']/field[@name='last_calculated_tax'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of
                                                    select="object[@model='crm.currency']/field[@name='short_name']"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                    <xsl:for-each select="object[@model='crm.textparagraphinsalesdocument']">
                        <xsl:choose>
                            <xsl:when test="field[@name='purpose']='AT'">
                                <fo:block font-size="9pt"
                                          font-family="BitstreamVeraSans"
                                          color="black"
                                          text-align="left"
                                          margin-top="2cm"
                                          linefeed-treatment="preserve">
                                    <xsl:value-of select="field[@name='text_paragraph']"/>
                                </fo:block>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:for-each>
                    <fo:block id="last-page"></fo:block>
                </fo:flow>
                <xsl:apply-templates/>
            </fo:page-sequence>
        </fo:root>
    </xsl:template>
</xsl:stylesheet>
