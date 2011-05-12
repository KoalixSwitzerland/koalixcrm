<xsl:stylesheet
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
     xmlns:fo="http://www.w3.org/1999/XSL/Format">
<xsl:decimal-format name="european" decimal-separator="," grouping-separator="."/>
<xsl:template match ="django-objects">
  <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
    <!-- defines page layout -->
    <fo:layout-master-set>
      <fo:simple-page-master master-name="simple"
                    page-height="29.7cm"
                    page-width="21cm"
                    margin-top="1.5cm"
                    margin-bottom="0.5cm"
                    margin-left="1.5cm"
                    margin-right="1.5cm">
        <fo:region-body margin-top="10.5cm" margin-bottom="1.5cm"/>
        <fo:region-before extent="10.5cm"/>
        <fo:region-after extent="1.5cm"/>
      </fo:simple-page-master>
    </fo:layout-master-set>
    <fo:page-sequence master-reference="simple">
      <fo:static-content flow-name="xsl-region-before" >
        <fo:table table-layout="fixed" width="100%">
          <fo:table-column column-width="18.0cm"/>
          <fo:table-body font-size="9pt"
                         font-family="BitstreamVeraSans">
          <fo:table-row height="2cm" border-bottom-color="black" border-bottom-style="solid" border-bottom-width="0.5pt">
            <fo:table-cell padding-bottom="3pt" >
              <fo:block text-align="left" >
                <fo:external-graphic src="/var/www/koalixcrm/logo.jpg" content-width="6.0cm"/>
              </fo:block>
            </fo:table-cell>
          </fo:table-row>
          </fo:table-body>
        </fo:table>
        <fo:table table-layout="fixed" width="100%" margin-top="1.5cm">
        <fo:table-column column-width="3cm"/>
        <fo:table-column column-width="7cm"/>
        <fo:table-column column-width="8cm"/>
        <fo:table-body font-size="7pt"
                       font-family="BitstreamVeraSans">
    <fo:table-row >
          <fo:table-cell>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              font-weight="bold">Erstelldatum:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Kundennummer:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Auftragsnummer:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">MwSt.-Nummer:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Postkonto:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Gültig bis:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Ansprechpartner:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Telefon Direkt:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">E-mail Direkt:</fo:block>
          </fo:table-cell>
          <fo:table-cell>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              font-weight="bold">
                <xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 1, 4)"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">KU-<xsl:value-of select="object[@model='crm.contact']/@pk"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">RE-<xsl:value-of select="object[@model='crm.salescontract']/field[@name='contract']"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">keine</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">PC 000054545</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='validuntil'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='validuntil'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='validuntil'], 1, 4)"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="object[@model='auth.user']/field[@name='first_name']"/>&#8201;  <xsl:value-of select="object[@model='auth.user']/field[@name='last_name']"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">+41(0)545878948</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="object[@model='auth.user']/field[@name='email']"/></fo:block>
          </fo:table-cell>
          <fo:table-cell>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              text-decoration="underline">Guest Guesterich,  Gueststreet, CH-9602 Bazenheid</fo:block>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <xsl:choose>
              <xsl:when  test="object[@model='crm.postaladdressforcontact']/field[@name='purpose']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='prename']"/>&#8201; <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='name']"/>
              </fo:block>
              <xsl:choose>
                <xsl:when test="object[@model='crm.postaladdress']/field[@name='addressline1']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='addressline1']"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="object[@model='crm.postaladdress']/field[@name='addressline2']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='addressline2']"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="object[@model='crm.postaladdress']/field[@name='addressline3']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='addressline3']"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="object[@model='crm.postaladdress']/field[@name='addressline4']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='addressline4']"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='zipcode']"/> &#8201;  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='town']"/>
              </fo:block>
            </xsl:when>
         </xsl:choose>
        </fo:table-cell>
       </fo:table-row>
    </fo:table-body>
       </fo:table>
        <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="1.0cm">&#8201; 
       </fo:block>
        <fo:block font-size="15pt"
              font-family="BitstreamVeraSans"
              color="black"
              text-align="left"
              font-weight="bold">
        Rechnung RE-<xsl:value-of select="object[@model='crm.salescontract']/@pk"/>
       </fo:block>
      </fo:static-content>
    <fo:static-content flow-name="xsl-region-after" >
       <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
       <fo:table table-layout="fixed" width="100%">
          <fo:table-column column-width="15.0cm"/>
          <fo:table-column column-width="3.0cm"/>
        <fo:table-body>
          <fo:table-row border-top-color="black" border-top-style="solid" border-top-width="0.5pt">
            <fo:table-cell number-columns-spanned="2">
            <fo:block font-size="5pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              font-weight="bold"
              >&#8201; </fo:block>
            </fo:table-cell>
          </fo:table-row>
         <fo:table-row>
           <fo:table-cell>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              font-weight="bold"
              text-align="start">Guest Guesterich &#8201;  &#8201;  &#8201;  &#8201; Gueststreet &#8201;  &#8201;  &#8201;  &#8201; 9602 Bazenheid &#8201;  &#8201;  &#8201;  &#8201; +41 (0)71 511 21 18 &#8201;  &#8201;  &#8201;  &#8201; info@koalix.com</fo:block>
           </fo:table-cell>
           <fo:table-cell>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              font-weight="bold"
              text-align="end">Seite <fo:page-number/>/<fo:page-number-citation ref-id="last-page"/></fo:block>
           </fo:table-cell>
         </fo:table-row>
        </fo:table-body>
       </fo:table> 
    </fo:static-content>
      <fo:flow flow-name="xsl-region-body">

       <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="13pt" >&#8201;  </fo:block>
       <fo:table table-layout="fixed" width="100%">
          <fo:table-column column-width="1.0cm"/>
          <fo:table-column column-width="8.4cm"/>
          <fo:table-column column-width="1.8cm"/>
          <fo:table-column column-width="2.5cm"/>
          <fo:table-column column-width="1.8cm"/>
          <fo:table-column column-width="2.5cm"/>
      <fo:table-header font-size="9pt" line-height="9pt" font-weight="bold" font-family="BitstreamVeraSans">
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      Pos.
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      Beschreibung
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Anzahl
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Einzelpreis
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Rabatt
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Betrag
                   </fo:block>
                </fo:table-cell>
             </fo:table-header>
          <fo:table-body font-size="9pt"
                         font-family="BitstreamVeraSans">
         <xsl:for-each select="object[@model='crm.position']">
          <xsl:sort select="field[@name=positionNumber]" data-type="number"/>
             <fo:table-row keep-together="always">
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      <xsl:value-of select="field[@name='positionNumber']"/>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      <xsl:value-of select="/object[@model='crm.product' and @pk='1']/field[@name='Title']"/>
                      <xsl:choose>
                         <xsl:when test="field[@name='description']">
                      <xsl:value-of select="field[@name='description']"/></xsl:when>
                         <xsl:otherwise>
                      <xsl:value-of select="field[@name='description']"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='description'] = '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(field[@name='quantity'], '#.##0,00', 'european')"/>&#8201;  <xsl:value-of select="uomDescription"/>&#8201; 
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='positionPricePerUnit']/None">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(field[@name='positionPricePerUnit'], '#.##0,00', 'european')"/>&#8201;<xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='discount']/None">-</xsl:when> 
                         <xsl:otherwise>
                              <xsl:value-of select="format-number(field[@name='discount'], '#.##0,00', 'european')"/> %
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='lastCalculatedPrice']/None">-</xsl:when>
                         <xsl:otherwise>
                           <xsl:value-of select="format-number(field[@name='lastCalculatedPrice'], '#.##0,00', 'european')"/>&#8201;<xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
            </xsl:for-each>
             <fo:table-row keep-together="always" keep-with-previous="always">
               <fo:table-cell number-columns-spanned="6"><fo:block  text-align="start" >&#8201; 
                   </fo:block></fo:table-cell>
             </fo:table-row>
              <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="2">
                   <fo:block  text-align="start" >&#8201; 
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      Zwischensumme
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                        <xsl:when test="object[@model='crm.salescontract']/field[@name='lastCalculatedPrice']/None">-</xsl:when>
                        <xsl:otherwise>
                        <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedPrice'], '#.##0,00', 'european')"/>&#8201;<xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
                        </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
             <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="2">
                   <fo:block  text-align="start" >
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                     MwSt.
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
             <xsl:choose>
               <xsl:when test="object[@model='crm.salescontract']/field[@name='lastCalculatedTax']/None">-</xsl:when>
               <xsl:otherwise>
               <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedTax'], '#.##0,00', 'european')"/>&#8201;<xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
               </xsl:otherwise>
             </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
             <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="2">
                   <fo:block  text-align="start" >
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" font-weight="bold">
                      Total
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" font-weight="bold">
             <xsl:choose>
               <xsl:when test="object[@model='crm.salescontract']/field[@name='lastCalculatedPrice']/None">-</xsl:when>
               <xsl:otherwise>
               <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedPrice']+object[@model='crm.salescontract']/field[@name='lastCalculatedTax'], '#.##0,00', 'european')"/>&#8201;<xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
               </xsl:otherwise>
             </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
          </fo:table-body>
       </fo:table>
              <fo:block font-size="10pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="0.5cm" >&#8201; 
             </fo:block>

              <fo:block font-size="10pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="13pt" >Freundliche Grüsse
             </fo:block>

              <fo:block font-size="10pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="20pt" >&#8201; 
             </fo:block>

              <fo:block font-size="10pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="13pt"
              id="last-page">Guest Guesterich
             </fo:block>
    </fo:flow>
     <xsl:apply-templates/>
  </fo:page-sequence>
  </fo:root>
</xsl:template>
</xsl:stylesheet>
