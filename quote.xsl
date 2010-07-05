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
                <fo:external-graphic src="/opt/koalix/vorlage/Pictures/logo.jpg" content-width="6.0cm"/>
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
              text-align="left">Zahlbar bis:</fo:block>
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
                <xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 1, 4)"/>
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
              text-align="left">PC 85-28819-4</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="substring(object[@model='crm.quote']/field[@name='validuntil'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.quote']/field[@name='validuntil'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.quote']/field[@name='validuntil'], 1, 4)"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="_object/salesRep/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_object/firstName"/>&#8201;  <xsl:value-of select="_object/salesRep/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_object/lastName"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">
            <xsl:for-each select="_object/salesRep/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PhoneNumber/_object">
              <xsl:choose>
                <xsl:when test="phoneNumberFull">
                  <xsl:value-of select="phoneNumberFull"/>
                </xsl:when>
              </xsl:choose>
            </xsl:for-each></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">
            <xsl:for-each select="_object/salesRep/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.EMailAddress/_object">
              <xsl:choose>
                <xsl:when test="emailAddress">
                  <xsl:value-of select="emailAddress"/>
                </xsl:when>
              </xsl:choose>
            </xsl:for-each></fo:block>
          </fo:table-cell>
          <fo:table-cell>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              text-decoration="underline">koalix GmbH, Nelkenstrasse 12, CH-9500 Wil SG</fo:block>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
            <xsl:choose>
              <xsl:when  test="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_object/lastName">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_object/firstName"/>&#8201; <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_object/lastName"/>
              </fo:block>
              <xsl:choose>
                <xsl:when test="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalStreet/_item[position()=1]">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalStreet/_item[position()=1]"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalStreet/_item[position()=2]">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
                  <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalStreet/_item[position()=2]"/>
              </fo:block>
                </xsl:when>
              </xsl:choose>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalCode"/> &#8201;  <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.Contact/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalCity"/>
              </fo:block>
            </xsl:when>
            <xsl:otherwise>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of  select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.LegalEntity/_object/fullName"/>
              </fo:block>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.LegalEntity/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalStreet/_item"/>
              </fo:block>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.LegalEntity/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalCode"/>&#8201;  <xsl:value-of select="_object/customer/segment/org.opencrx.kernel.account1.Segment/_content/account/org.opencrx.kernel.account1.LegalEntity/_content/address/org.opencrx.kernel.account1.PostalAddress/_object/postalCity"/>
              </fo:block>
           </xsl:otherwise>
         </xsl:choose>
        </fo:table-cell>
        </fo:table-row>
        <fo:table-row >
          <fo:table-cell number-columns-spanned="2">
            <fo:block font-size="14pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201; </fo:block>
	  <xsl:for-each select="_content/address/org.opencrx.kernel.contract1.PostalAddress/_object">
           <xsl:choose>
            <xsl:when test="usage/_item = '10200'">
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Lieferanschrift:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:choose>
                <xsl:when test="postalStreet/_item[position()=1] != ''">
                  <xsl:value-of select="postalStreet/_item[position()=1]"/>,
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="postalStreet/_item[position()=2] != ''">
                  <xsl:value-of select="postalStreet/_item[position()=2]"/>,
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="postalStreet/_item[position()=3] != ''">
                  <xsl:value-of select="postalStreet/_item[position()=3]"/>,
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="postalStreet/_item[position()=4] != ''">
                  <xsl:value-of select="postalStreet/_item[position()=4]"/>,
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="postalCode">
                  <xsl:value-of select="postalCode"/>&#8201; 
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="postalCity">
                  <xsl:value-of select="postalCity"/>
                </xsl:when>
              </xsl:choose></fo:block>
            </xsl:when>
           </xsl:choose>
	  </xsl:for-each>
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
        Rechnung RE-<xsl:value-of select="_object/contractNumber"/>
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
              text-align="start">koalix GmbH &#8201;  &#8201;  &#8201;  &#8201; Nelkenstrasse 12 &#8201;  &#8201;  &#8201;  &#8201; 9500 Wil &#8201;  &#8201;  &#8201;  &#8201; +41 (0)71 511 21 18 &#8201;  &#8201;  &#8201;  &#8201; info@koalix.com</fo:block>
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
	  <xsl:for-each select="_content/note/org.opencrx.kernel.generic.Note/_object">
           <xsl:choose>
            <xsl:when test="title = 'Begrüssung'">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:choose>
                <xsl:when test="text">
                  <xsl:value-of select="text"/>
                </xsl:when>
              </xsl:choose>
             </fo:block>
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">&#8201;  </fo:block>
            </xsl:when>
           </xsl:choose>
	  </xsl:for-each>
	  <xsl:for-each select="_content/note/org.opencrx.kernel.generic.Note/_object">
           <xsl:choose>
            <xsl:when test="title = 'Einführung'">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:choose>
                <xsl:when test="text">
                  <xsl:value-of select="text"/>
                </xsl:when>
              </xsl:choose>
             </fo:block>
            </xsl:when>
           </xsl:choose>
	  </xsl:for-each>

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
         <xsl:for-each select="_content/position/org.opencrx.kernel.contract1.InvoicePosition/_object">
          <xsl:sort select="positionNumber" data-type="number"/>
             <fo:table-row keep-together="always">
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      <xsl:value-of select="positionNumber"/>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      <xsl:choose>
                         <xsl:when test="description">
                      <xsl:value-of select="description"/></xsl:when>
                         <xsl:otherwise>
                      <xsl:value-of select="productDetailedDescription"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="quantity = '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(quantity, '#.##0,00', 'european')"/>&#8201;  <xsl:value-of select="uomDescription"/>&#8201; 
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="pricePerUnit = '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(pricePerUnit, '#.##0,00', 'european')"/> CHF
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="discountAmount = '0E-15'">-</xsl:when> 
                         <xsl:otherwise>
                            <xsl:choose>
                              <xsl:when test="discountIsPercentage = 'true'">
                                <xsl:value-of select="format-number(discount, '#.##0,00', 'european')"/> %
                              </xsl:when>
                              <xsl:otherwise>
                                <xsl:value-of select="format-number(discountAmount, '#.##0,00', 'european')"/> CHF
                              </xsl:otherwise>
                            </xsl:choose>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="baseAmount = '0E-15'">-</xsl:when>
			 <xsl:when test="discountAmount = '0E-15'">
                           <xsl:value-of select="format-number(baseAmount, '#.##0,00', 'european')"/> CHF
                         </xsl:when>
                         <xsl:otherwise>
                           <xsl:variable  name="amountWithDiscount"><xsl:value-of select="baseAmount - discountAmount"/></xsl:variable>
                           <xsl:value-of select="format-number($amountWithDiscount, '#.##0,00', 'european')"/> CHF
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
                         <xsl:when test="_object/totalAmount= '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(_object/totalAmount, '#.##0,00', 'european')"/> CHF
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
                         <xsl:when test="_object/totalTaxAmount = '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(_object/totalTaxAmount, '#.##0,00', 'european')"/> CHF
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
                   <fo:block  text-align="start" >Akonto</fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
             <xsl:choose>
               <xsl:when test="_object/userNumber0 = '0E-15'">-</xsl:when>
               <xsl:otherwise>
               <xsl:value-of select="format-number(_object/userNumber0, '#.##0,00', 'european')"/> CHF
               </xsl:otherwise>
             </xsl:choose></fo:block>
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
                   <fo:block  text-align="end" font-weight="bold"><xsl:choose>
                <xsl:when test="_object/totalAmountIncludingTax = '0E-15'">-</xsl:when>
		<xsl:when test="_object/userNumber0 = '0E-15'">
                  <xsl:value-of select="format-number(_object/totalAmountIncludingTax, '#.##0,00', 'european')"/> CHF
                </xsl:when>
                <xsl:otherwise>
                  <xsl:variable  name="totalamountwithakonto"><xsl:value-of select="_object/totalAmountIncludingTax - _object/userNumber0"/></xsl:variable>
                  <xsl:value-of select="format-number($totalamountwithakonto, '#.##0,00', 'european')"/> CHF
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
	  <xsl:for-each select="_content/note/org.opencrx.kernel.generic.Note/_object">
           <xsl:choose>
            <xsl:when test="title = 'Endtext'">
              <fo:block font-size="10pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="13pt" 
              margin-bottom="20pt">
              <xsl:choose>
                <xsl:when test="text">
                  <xsl:value-of select="text"/>
                </xsl:when>
              </xsl:choose>
             </fo:block>
            </xsl:when>
           </xsl:choose>
	  </xsl:for-each>

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
              id="last-page">Aaron Riedener
             </fo:block>
    </fo:flow>
     <xsl:apply-templates/>
  </fo:page-sequence>
  </fo:root>
</xsl:template>
</xsl:stylesheet>
