<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng"
				version="1.0">
<xsl:output method="xml" encoding="UTF-8" indent="no"
	doctype-public="-//W3C//DTD XHTML 1.1//EN"
	doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />

<!--
	This XSL file is an example to illustrate how to implement dictionary-specific preferences.
	This file is not necessary if you don't need preference for the dictionary.
	
	This XSL does the followings.
	- Add style to mask unwanted pronunciation formats. 
	- $pronunciation is externally provided.
-->

<xsl:template match="*[@id='c']">
	<xsl:if test="$ShowCopyright = '1'">
		<xsl:copy>
			<xsl:attribute name="style" select="@*|node()">display:block</xsl:attribute>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
</xsl:template>
<xsl:template match="*[@id='u1']">
	<xsl:if test="$CheckForUpdates = '1'">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
	<xsl:if test="$CheckForUpdates = '2'">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
</xsl:template>
<xsl:template match="*[@id='u2']">
	<xsl:if test="$CheckForUpdates = '2'">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:if>
</xsl:template>

<!--
	Default rule for all other tags
-->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()" />
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
