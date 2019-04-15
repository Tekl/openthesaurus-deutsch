#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DIESES SCRIPT BITTE NICHT MANUELL AUSFÜHREN
# ES WIRD PER "MAKE" AUFGERUFEN

import os,sys,time,re,codecs,datetime,urllib,string,subprocess,pickle,email,time,copy

def progress(a,b,c):
    sys.stdout.write(".")

def sort_by_value(d):
    """ Returns the keys of dictionary d sorted by their values """
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

def normalize(s):
    s = s.replace(u"ä","a")
    s = s.replace(u"ö","o")
    s = s.replace(u"ü","u")
    s = s.replace(u"Ä","A")
    s = s.replace(u"Ö","O")
    s = s.replace(u"Ü","U")
    return s

os.system("clear")

print "Lexikon-Plugin auf Basis von OpenThesaurus.de"
print "CreateXML v2.0.0 von Wolfgang Reszel, 2019-04-10"
print
morphology = {}
for file in ["morphology-cache.txt","../Morphologie_Deutsch/morphology-cache.txt"]:
    if os.path.isfile(file):
        print "Morpholgie-Cache-Datei gefunden und geladen.\n"
        morphcache = open(file,'r')
        morphology = pickle.load(morphcache)
        morphcache.close()
        for id in morphology:
            morphology[id] = re.sub(r'^(Adjektiv,|Substantiv,|Verb,)','',morphology[id])
            morphology[id] = re.sub(r'^([^,]+)(Adjektiv,|Substantiv,|Verb,)',r'\1,',morphology[id])
        break

print "Aktueller Thesaurus wird herunterladen ",

bundleVersion = datetime.datetime.today().strftime("%Y.%m.%d")

urllib.urlcleanup()
download = urllib.urlretrieve("http://www.openthesaurus.de/export/OpenThesaurus-Textversion.zip","thesaurus.txt.zip",progress)

if string.find(str(download[1]),"Error") > -1 or string.find(str(download[1]),"Content-Type: application/zip") == -1:
    print download[1]
    sys.exit("Herunterladen fehlgeschlagen, bitte später noch mal versuchen")

timestamp = re.sub("(?s)^.*Last-Modified: ([^\n]+)\n.*$","\\1",str(download[1]))
downloadfiledate = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%d.%m.%Y")
downloadfileyear = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%Y")

print "\nHeruntergeladene Datei wird entpackt ..."
os.system('unzip -o thesaurus.txt.zip')

print "\nDatei wird analysiert ..."
sourcefile = codecs.open('openthesaurus.txt','r','UTF-8')
result = {}
dvalues = {}
titles = {}
headlines = {}
lengths = {}
linkwords = {}
wordcount = 0
dvaluesplain = {}

speedvar = ""

for line in sourcefile:
    if line[0] == "#":
        continue

    line = line.strip()
    if '"' in line:
        line = re.sub(';([^;"]+) "([^;"]+)"([^;]*);',";\\1 \\2\\3;\\2\\3;", line)

   #speedup
    if speedvar != "":
        if speedvar in line:
            print line
            pass
        else:
            continue

    elements = line.split(";")

    for element in elements:
        if element == "":
            continue

        #wordcount+=1

        element = element.replace("&","&amp;")
        element = element.replace("<","&lt;")
        element = element.replace(">","&gt;")
        element = element.replace("\"","")
        translations = ""
        for i in elements:
            if i == "":
                continue
            if i != element:
                i = i.replace("&","&amp;")
                i = i.replace("<","&lt;")
                i = i.replace(">","&gt;")
                i = i.replace("\"","")
                translations = translations + "; " + i

        translations = translations[2:len(translations)]
        translations = re.sub('(\([^)]+\))', '<i>\\1</i>',translations)
        translations = re.sub('> *<',u'> <',translations).strip() # six-per-em space U+2006

        id = re.sub('(?u)[\"<>, ]','_',element.lower())
        id = re.sub("(?u)_+","_",id)
        id = re.sub("(?u)(.)_$","\\1",id)

        dvalue = re.sub('\([^)]+\)',"",element).strip()
        dvalue = re.sub('  +','',dvalue).strip()
        dvalue = dvalue[:127]

        if dvalue == "":
            dvalue = id[:127]

        if result.has_key(id):
            if translations.lower() not in result[id].lower():
                result[id] = result[id] + "\n<p>" + translations + "</p>"
        else:
            lengths[id] = len(id)
            result[id] = "<p>" + translations + "</p>"
            dvalues[id] = u'\n<d:index d:value="'+dvalue+u'" d:title="'+dvalue+u'"/>'
            titles[id] = element
            dvaluesplain[id] = dvalue
            linkwords[id] = urllib.quote(re.sub('\([^)]+\)|{[^}]+}|\[[^\]]+\]',"",element).strip().encode("utf-8"))
            headlines[id] = re.sub('(\([^)]+\))', '<i>\\1</i>',element)
            headlines[id] = re.sub('> *<',u'> <',headlines[id]).strip() # six-per-em space U+2006
            if morphology.has_key(dvalue):
                for x in morphology[dvalue].split(","):
                    if u'\n<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                        if x.lower() > dvalue.lower():
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                        else:
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+dvalue+u' ← '+x+u'"/>'
                        # if x[:len(dvalue)].lower() == dvalue.lower():
                        #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                        # else:
                        #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'

        dvalueSplit = dvalue.split()
        for i in dvalueSplit:
            if len(i) > 1:
                devalueHyphenSplit = i.split("-")
                for j in range(1,len(devalueHyphenSplit)):
                    if len(devalueHyphenSplit[j]) > 1:
                        if u'\n<d:index d:value="'+normalize(devalueHyphenSplit[j].lower())+u'"' not in normalize(dvalues[id].lower()):
                            if devalueHyphenSplit[j].lower() > dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+devalueHyphenSplit[j]+u'" d:title="'+devalueHyphenSplit[j]+u' → '+dvalue+u'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+devalueHyphenSplit[j]+u'" d:title="'+dvalue+u' ← '+devalueHyphenSplit[j]+u'"/>'
                            # dvalues[id] = dvalues[id] + '\n<d:index d:value="'+devalueHyphenSplit[j]+u'" d:title="'+devalueHyphenSplit[j]+u' ⇒ '+dvalue+u'"/>'
                        if morphology.has_key(devalueHyphenSplit[j]):
                            for x in morphology[devalueHyphenSplit[j]].split(","):
                                if u'\n<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                                    if x.lower() > dvalue.lower():
                                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                                    else:
                                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+dvalue+u' ← '+x+u'"/>'
                                    # if x[:len(dvalue)].lower() == dvalue.lower():
                                    #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                                    # else:
                                    #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'
                if '\n<d:index d:value="'+normalize(i.lower())+'"' not in normalize(dvalues[id].lower()):
                    if i[0] != "-" and i[len(i)-1] != "-":
                        if dvalue[:len(i)].lower() != i.lower():
                            if i.lower() > dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+i+u'" d:title="'+i+u' ⇒ '+dvalue+u'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+i+u'" d:title="'+dvalue+u' ← '+i+u'"/>'
                            # dvalues[id] = dvalues[id] + '\n<d:index d:value="'+i+u'" d:title="'+i+u' ⇒ '+dvalue+u'"/>'
                        if morphology.has_key(i):
                            for x in morphology[i].split(","):
                                if u'\n<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                                    if x.lower() > dvalue.lower():
                                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                                    else:
                                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+dvalue+u' ← '+x+u'"/>'
                                    # if x[:len(dvalue)].lower() == dvalue.lower():
                                    #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                                    # else:
                                    #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'


sourcefile.close()
lengths2 = copy.copy(lengths)

for id in lengths2:
    id2 = re.sub('(.+)(\(|\))',"\\1",id)

    if id != id2 and result.has_key(id2) and result.has_key(id):
        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if morphology.has_key(id) and result.has_key(id):
        for x in morphology[id].split(","):
            if x != id and result.has_key(x):
                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'

    id2 = re.sub('_*\([^)]+\)_*',"",id)
    id2 = re.sub('^(der|die|das|den|dem|des|an|am|sein|ein|etwas|[enmr]*)_[a-z]+_([a-z]+)$',"\\2",id2)
    id2 = re.sub('(_|^)(jemand[ensr]*|eigen[res]*|der|die|das|dem|den|des[sen]*|vo[nm]|ein[ermns]*)(_|$)',"",id2)
    id2 = re.sub('^(in|im|ein|wo|an|am|hat|hatte|er|sie|es|ich|du|es|ihm|ihr|sich|sein|wird|wurde|war|sich|alle[nrs]*|nicht|kein[er]*|ohne|mit|total)_',"",id2)
    id2 = re.sub('_([a-z]*lassen$|w[eu]rden|ge[a-z]+|können|er[a-z]+|[a-z]+en)$',"",id2)

    if id != id2 and result.has_key(id2) and result.has_key(id):
        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if morphology.has_key(id) and result.has_key(id):
        for x in morphology[id].split(","):
            if x != id and result.has_key(x):
                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'

    id2 = re.sub('_*\([^)]+\)_*',"",id)
    id2 = re.sub('^[a-z]+_([a-z]+)$',"\\1",id2)

    if id != id2 and result.has_key(id2) and result.has_key(id):
        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if morphology.has_key(id) and result.has_key(id):
        for x in morphology[id].split(","):
            if x != id and result.has_key(x):
                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if '<a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>','') + ', <a href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'


print "\nXML-Datei wird erzeugt ..."
destfile = codecs.open('ThesaurusDeutsch.xml','w','utf-8')
destfile.write("""<?xml version="1.0" encoding="utf-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">""")

for id in lengths:
    wordcount+=1
    destfile.write( re.sub("  +","", u"""
<d:entry id="%s" class="d" d:title="%s">%s
<h2 d:pr="1">%s</h2>
%s
<div class="c" d:priority="2"><span><a href="https://www.openthesaurus.de/synonyme/%s">Aus OpenThesaurus.de</a> · © %s Daniel Naber</span></div>
</d:entry>
""" % (id, titles[id], dvalues[id], headlines[id], result[id], linkwords[id], downloadfileyear ) ) )

destfile.write( u"""
<d:entry id="front_back_matter" d:title="Vorderer/hinterer Teil">
    <h1>OpenThesaurus Deutsch</h1>
    <div><small><b>Version: %s</b></small></div>
    <p>
        Dieser Thesaurus basiert auf dem Online-Thesaurus<br/>
        <a href="https://www.openthesaurus.de">www.openthesaurus.de</a> von Daniel Naber. (Stand: %s, %s Einträge)
    </p>
    <p>
        <b>Updates</b> finden Sie unter <a href="https://www.tekl.de">www.tekl.de</a>.<br/>
        Support und den Quellcode finden Sie unter <a href="https://github.com/Tekl/openthesaurus-deutsch"><b>github.com/Tekl/openthesaurus-deutsch</b></a>.
    </p>
    <p>
        Das Python-Skript zur Umwandlung der OpenThesaurus-Wortliste in ein Lexikon-Plugin wurde von Wolfgang Reszel entwickelt.
    </p>
    <p>
        Die Wortform-Datei (Morphologie), durch welche auch die Suche nach Worten im Plural möglich ist, wurde mit dem Windows-Tool <a href="http://morphy.wolfganglezius.de">Morphy</a> erstellt.
    </p>
    <p>
        <img src="Images/gplv3-88x31.png" align="left" style="padding-right:10px" alt=""/>
        <b>Lizenz:</b>
        Dieses Lexikon-Plug-in unterliegt der <a href="https://www.gnu.org/licenses/gpl.html">GPLv3</a><br/>
        Die Wortliste von OpenThesaurus unterliegt der
        <a href="https://creativecommons.org/licenses/LGPL/2.1/">CC-GNU LGPL</a><br/>
    </p>
</d:entry>
</d:dictionary>""" % (bundleVersion, downloadfiledate, wordcount ) )
destfile.close()

print "\nHeruntergeladene Datei wird gelöscht ..."
os.system("rm openthesaurus.txt")
os.system("rm thesaurus.txt.zip")
os.system("rm LICENSE.txt")

print "\nVersionsnummern werden angepasst ..."
rtfFiles = ['installer/finishup_de.rtfd/TXT.rtf','installer/finishup_en.rtfd/TXT.rtf','installer/LIESMICH.rtfd/TXT.rtf','installer/README.rtfd/TXT.rtf','LIESMICH.md','README.md','Makefile']
for filename in rtfFiles:
	print filename
	if '.rtf' in filename:
		pmdocFile = codecs.open(filename,'r','windows-1252')
	else:
		pmdocFile = codecs.open(filename,'r','UTF-8')
	pmdoc = pmdocFile.read()
	pmdoc = re.sub("Version: .\d+.\d+.\d+", "Version: "+ bundleVersion, pmdoc)
	pmdoc = re.sub(" 20\d+.\d+.\d+\"", " "+ bundleVersion+"\"", pmdoc)
	pmdoc = re.sub(" v20\d+.\d+.\d+\"", " v"+ bundleVersion+"\"", pmdoc)
	if filename == 'Makefile':
		pmdoc = re.sub("([_ ])v20\d+.\d+.\d+", "\\1v"+ bundleVersion+"", pmdoc)
		pmdoc = re.sub("/20\d+.\d+.\d+/", "/"+ bundleVersion+"/", pmdoc)
	pmdoc = re.sub(u"20\d\d Wolfgang Reszel", datetime.datetime.today().strftime("%Y")+" Wolfgang Reszel", pmdoc)
	pmdocFile.close()
	if '.rtf' in filename:
		pmdocFile = codecs.open(filename,'w','windows-1252')
	else:
		pmdocFile = codecs.open(filename,'w','UTF-8')
	pmdocFile.write( pmdoc )
	pmdocFile.close()

print "Info.plist"
plistFile = codecs.open('Info.plist','r','UTF-8')
plist = plistFile.read()
plist = re.sub("(?u)(<key>CFBundleVersion</key>\s+<string>)[^<]+(</string>)", "\\g<1>"+bundleVersion+"\\2", plist)
plist = re.sub("(?u)(<key>CFBundleShortVersionString</key>\s+<string>)[^<]+(</string>)", "\\g<1>"+bundleVersion+"\\2", plist)
plist = re.sub(u"© \d\d\d\d ", u"© "+ datetime.datetime.today().strftime("%Y")+u" ", plist)
plistFile.close()
plistFile = codecs.open('Info.plist','w','UTF-8')
plistFile.write( plist )
plistFile.close()

print "\nXML-Datei wird ausgewertet (Making) ...\n-----------------------------------------------------"
