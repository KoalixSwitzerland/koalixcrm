<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
     xmlns:fo="http://www.w3.org/1999/XSL/Format">
<xsl:output method="xml" version="1.0" indent="yes" encoding="UTF-8"/>
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
                <fo:external-graphic content-width="6.0cm">
                  <xsl:attribute name="src">
                     <xsl:value-of select="filebrowserdirectory"/><xsl:value-of select="object[@model='djangoUserExtension.templateset']/field[@name='logo']"/>
                  </xsl:attribute>
                </fo:external-graphic>
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
              font-weight="bold">Created at:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:text> </xsl:text> </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Customer Nr:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Contract Nr:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:text> </xsl:text> </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Tax Ref Nr:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">IBAN:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Payable until:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:text> </xsl:text> </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Responsible Person:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">Phone direkt:</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">E-mail direkt:</fo:block>
          </fo:table-cell>
          <fo:table-cell>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              font-weight="bold">
                <xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.salescontract']/field[@name='dateofcreation'], 1, 4)"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><fo:leader leader-pattern="space"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">CU-<xsl:value-of select="object[@model='crm.contact']/@pk"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">CO-<xsl:value-of select="object[@model='crm.salescontract']/field[@name='contract']"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><fo:leader leader-pattern="space"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">none</fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left">
            <xsl:choose>
	      <xsl:when  test="object[@model='djangoUserExtention.templateset']/field[@name='bankingaccountref']">
		<xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='bankingaccountref']"/>
	      </xsl:when>
	      <xsl:otherwise>
		<fo:leader leader-pattern="space"/>
	      </xsl:otherwise>
            </xsl:choose>
            </fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='payableuntil'], 9, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='payableuntil'], 6, 2)"/><xsl:text>.</xsl:text><xsl:value-of select="substring(object[@model='crm.invoice']/field[@name='payableuntil'], 1, 4)"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><fo:leader leader-pattern="space"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="object[@model='auth.user']/field[@name='first_name']"/><xsl:text> </xsl:text>  <xsl:value-of select="object[@model='auth.user']/field[@name='last_name']"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="object[@model='crm.phoneaddress']/field[@name='phone']"/></fo:block>
            <fo:block font-size="7pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:value-of select="object[@model='auth.user']/field[@name='email']"/></fo:block>
          </fo:table-cell>
          <fo:table-cell>
            <fo:block font-size="6pt"
              font-family="BitstreamVeraSans"
	      text-decoration="underline"
              text-align="start"
	      margin-bottom="0.5cm"><xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='addresser']"/></fo:block>
            <xsl:choose>
              <xsl:when  test="object[@model='crm.postaladdressforcontact']/field[@name='purpose']">
              <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left">
              <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='prename']"/><xsl:text> </xsl:text> <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='name']"/>
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
              <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='zipcode']"/> <xsl:text> </xsl:text>  <xsl:value-of select="object[@model='crm.postaladdress']/field[@name='town']"/>
              </fo:block>
            </xsl:when>
         </xsl:choose>
        </fo:table-cell>
       </fo:table-row>
   </fo:table-body>
       </fo:table>
        <fo:block font-size="15pt"
              font-family="BitstreamVeraSans"
              color="black"
              text-align="left"
              font-weight="bold"
              margin-top="1cm">
        Invoice IN-<xsl:value-of select="object[@model='crm.salescontract']/@pk"/>
       </fo:block>
        <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              color="black"
              text-align="left"
              margin-top="1cm">
       <xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='headerTextsalesorders']"/>
       </fo:block>
      </fo:static-content>
    <fo:static-content flow-name="xsl-region-after" >
       <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              text-align="left"><xsl:text> </xsl:text> </fo:block>
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
              ><xsl:text> </xsl:text> </fo:block>
            </fo:table-cell>
          </fo:table-row>
         <fo:table-row>
           <fo:table-cell>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              font-weight="bold"
              text-align="start">
               <xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='pagefooterleft']"/>
              <xsl:text>                  </xsl:text>
              <xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='pagefootermiddle']"/></fo:block>
           </fo:table-cell>
           <fo:table-cell>
            <fo:block font-size="8pt"
              font-family="BitstreamVeraSans"
              font-weight="bold"
              text-align="end">Page <fo:page-number/>/<fo:page-number-citation ref-id="last-page"/></fo:block>
           </fo:table-cell>
         </fo:table-row>
        </fo:table-body>
       </fo:table> 
    </fo:static-content>
      <fo:flow flow-name="xsl-region-body">

       <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              text-align="left"
              line-height="13pt" ><xsl:text> </xsl:text>  </fo:block>
       <fo:table table-layout="fixed" width="100%">
          <fo:table-column column-width="1.0cm"/>
          <fo:table-column column-width="6.6cm"/>
          <fo:table-column column-width="1.8cm"/>
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
                      Description
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Quantity
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Unit
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Price per Unit
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Discount
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      Amount
                   </fo:block>
                </fo:table-cell>
             </fo:table-header>
          <fo:table-body font-size="9pt"
                         font-family="BitstreamVeraSans">
         <xsl:for-each select="object[@model='crm.position']">
          <xsl:sort select="field[@name=positionNumber]" data-type="number"/>
             <fo:table-row >
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      <xsl:value-of select="field[@name='positionNumber']"/>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block-container max-width="6.0cm">
                   <xsl:variable name ="productinthisposition" select="field[@name='product']"/>
                   <fo:block  text-align="start"
                              font-weight="bold"
                              font-size="9pt"
                              font-family="BitstreamVeraSans"
                              line-height="12pt">
                      <xsl:value-of select="../object[@model='crm.product' and @pk=$productinthisposition]/field[@name='title']"/>
                   </fo:block>
                      <xsl:choose>
                         <xsl:when test="../object[@model='crm.product' and @pk=$productinthisposition]/field[@name='description']/None">
                           <fo:block  text-align="start"
                                       font-size="7pt"
                                       font-family="BitstreamVeraSans"
                              white-space-collapse="false">
                           <xsl:value-of select="field[@name='description']"/>
                           </fo:block>
                         </xsl:when>
                         <xsl:otherwise>
                           <fo:block  text-align="start"
                                       font-size="7pt"
                                       font-family="BitstreamVeraSans">
                           <xsl:value-of select="../object[@model='crm.product' and @pk=$productinthisposition]/field[@name='description']"/>
                           </fo:block>
                           <fo:block  text-align="start"
                                       font-size="7pt"
                                       font-family="BitstreamVeraSans"
                                       padding-top="0.1cm">
                           <xsl:value-of select="field[@name='description']"/>
                           </fo:block>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block-container>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='description'] = '0E-15'">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(field[@name='quantity'], '#.##0,00', 'european')"/><xsl:text> </xsl:text>  <xsl:value-of select="uomDescription"/><xsl:text> </xsl:text> 
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:variable name ="unitinthisposition" select="field[@name='unit']"/>
                      <xsl:choose>
                         <xsl:when test="field[../object[@model='crm.unit' and @pk=$unitinthisposition]/field[@name='shortName']/None]">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="../object[@model='crm.unit' and @pk=$unitinthisposition]/field[@name='shortName']"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                         <xsl:when test="field[@name='positionPricePerUnit']/None">-</xsl:when>
                         <xsl:otherwise>
                            <xsl:value-of select="format-number(field[@name='positionPricePerUnit'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
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
                           <xsl:value-of select="format-number(field[@name='lastCalculatedPrice'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of select="../object[@model='crm.currency']/field[@name='shortName']"/>
                         </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
            </xsl:for-each>
             <fo:table-row keep-together="always" keep-with-previous="always">
               <fo:table-cell number-columns-spanned="7"><fo:block  text-align="start" margin-top="0.5cm"><xsl:text> </xsl:text> 
                   </fo:block></fo:table-cell>
             </fo:table-row>
              <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="3">
                   <fo:block  text-align="start" ><xsl:text> </xsl:text> 
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                      Subtotal
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
                      <xsl:choose>
                        <xsl:when test="object[@model='crm.salescontract']/field[@name='lastCalculatedPrice']/None">-</xsl:when>
                        <xsl:otherwise>
                        <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedPrice'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of select="object[@model='crm.currency']/field[@name='shortName']"/>
                        </xsl:otherwise>
                      </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
             <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="3">
                   <fo:block  text-align="start" >
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="start" >
                     Tax
                   </fo:block>
                </fo:table-cell>
                <fo:table-cell number-columns-spanned="2" border-color="black" border-style="solid" border-width="0.5pt" padding="2.5pt">
                   <fo:block  text-align="end" >
             <xsl:choose>
               <xsl:when test="object[@model='crm.salescontract']/field[@name='lastCalculatedTax']/None">-</xsl:when>
               <xsl:otherwise>
               <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedTax'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of select="object[@model='crm.currency']/field[@name='shortName']"/>
               </xsl:otherwise>
             </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
             <fo:table-row keep-together="always" keep-with-previous="always">
                <fo:table-cell number-columns-spanned="3">
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
               <xsl:value-of select="format-number(object[@model='crm.salescontract']/field[@name='lastCalculatedPrice']+object[@model='crm.salescontract']/field[@name='lastCalculatedTax'], '#.##0,00', 'european')"/><xsl:text> </xsl:text><xsl:value-of select="object[@model='crm.currency']/field[@name='shortName']"/>
               </xsl:otherwise>
             </xsl:choose>
                   </fo:block>
                </fo:table-cell>
             </fo:table-row>
          </fo:table-body>
       </fo:table>
        <fo:block font-size="9pt"
              font-family="BitstreamVeraSans"
              color="black"
              text-align="left"
              margin-top="1cm"
              id="last-page">
      <xsl:value-of select="object[@model='djangoUserExtention.templateset']/field[@name='footerTextsalesorders']"/>
      </fo:block>
    </fo:flow>
     <xsl:apply-templates/>
  </fo:page-sequence>
  </fo:root>
</xsl:template>
</xsl:stylesheet>
