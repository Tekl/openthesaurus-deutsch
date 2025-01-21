<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng"
				version="1.0">
<xsl:output method="xml" encoding="UTF-8" indent="no"
	doctype-public="-//W3C//DTD XHTML 1.1//EN"
	doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />

<xsl:template match="div[@class='c']">
	<xsl:if test="$ShowCopyright = '1'">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
</xsl:template>

<xsl:template match="d:entry">
	<xsl:if test="$Font = '0'">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '1'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'American Typewriter'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '2'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Arial Narrow'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '3'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Avenir'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '4'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Avenir Next Condensed'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '5'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Baskerville'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '6'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Charter'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '7'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Cochin'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '8'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Geneva''</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '9'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Georgia''</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '10'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Graphik Compact'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '11'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Helvetica Neue'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '12'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Hoefler Text'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '13'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Kefa'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '14'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Lucida Grande'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '15'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Menlo'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '16'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Monaco'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '17'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Optima'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '18'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Palatino'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '19'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'PragmataPro'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '20'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'PT Sans'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '21'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'SF Compact'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '22'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'SF Compact Rounded'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '23'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'SF Pro'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '24'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'SF Pro Rounded'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '25'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Sys'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '26'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Tahoma'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '27'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Times New Roman'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '28'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Verdana'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '29'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: ui-serif</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '30'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: ui-sans-serif'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '31'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: ui-rounded</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '32'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: ui-monospace</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '33'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Marker Felt'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '34'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Chalkboard'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '35'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Comic Sans MS'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$Font = '36'">
		<xsl:copy>
			<xsl:attribute name="style">font-family: 'Rockwell'</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
</xsl:template>

<!-- Default rule for all other tags -->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
