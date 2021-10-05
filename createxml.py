#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DIESES SCRIPT BITTE NICHT MANUELL AUSFÜHREN
# ES WIRD PER "MAKE" AUFGERUFEN

import os, sys, time, re, codecs, datetime, copy, urllib, string, pickle, email  # , subprocess, time


def progress(a, b, c):
    sys.stdout.write(".")


def sort_by_value(d):
    """ Returns the keys of dictionary d sorted by their values """
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]


def normalize(s):
    s = s.replace(u"ä", "a")
    s = s.replace(u"ö", "o")
    s = s.replace(u"ü", "u")
    s = s.replace(u"Ä", "A")
    s = s.replace(u"Ö", "O")
    s = s.replace(u"Ü", "U")
    return s


os.system("clear")

if sys.argv[1] == "beta":
    versionSuffx = "-beta"
else:
    versionSuffx = ""

print("Lexikon-Plug-in (OpenThesaurus Deutsch) auf Basis von OpenThesaurus.de")
print("CreateXML v2.0.3 von Wolfgang Reszel, 2021-10-05")
print
morphology = {}
for file in ["morphology-cache.txt", "../Morphologie_Deutsch/morphology-cache.txt"]:
    if os.path.isfile(file):
        print("Morpholgie-Cache-Datei gefunden und geladen.\n")
        morphcache = open(file, 'r')
        morphology = pickle.load(morphcache)
        morphcache.close()
        break

print("Aktueller Thesaurus wird heruntergeladen ...")

bundleVersion = datetime.datetime.today().strftime("%Y.%m.%d") + versionSuffx

urllib.urlcleanup()
download = urllib.urlretrieve("https://www.openthesaurus.de/export/OpenThesaurus-Textversion.zip", "thesaurus.txt.zip", progress)

if string.find(str(download[1]), "Error") > -1 or string.find(str(download[1]), "Content-Type: application/zip") == -1:
    print(download[1])
    sys.exit("Herunterladen fehlgeschlagen, bitte später noch mal versuchen")

timestamp = re.sub(r"(?s)^.*Last-Modified: ([^\n]+)\n.*$", "\\1", str(download[1]))
downloadfiledate = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%d.%m.%Y")
downloadfileyear = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%Y")

print("\nHeruntergeladene Datei wird entpackt ...")
os.system('unzip -o thesaurus.txt.zip')

print("\nDatei wird analysiert ...")
sourcefile = codecs.open('openthesaurus.txt', 'r', 'UTF-8')
result = {}
dvalues = {}
parentals = {}
titles = {}
headlines = {}
lengths = {}
linkwords = {}
wordcount = 0
dvaluesplain = {}
parentalControlWords = {"(vulg.)", "(derb)", "(vulg., ", "(derb, ", ", vulg.)", ", derb)"}

speedvar = ""

abbreviations = {
    u"ugs.": u"umgangssprachlich",
    u"fig.": u"figurativ; übertragen; bildlich",
    u"geh.": u"gehoben",
    u"fachspr.": u"fachsprachlich",
    u"lat.": u"lateinisch",
    u"ital.": u"italienisch",
    u"bayr.": u"bayrisch",
    u"österr.": u"österreichisch",
    u"schweiz.": u"schweizerisch",
    u"fränk.": u"fränkisch",
    u"franz.": u"französisch",
    u"süddt.": u"süddeutsch",
    u"ruhrdt.": u"ruhrdeutsch",
    u"männl.": u"männliche Form",
    u"weibl.": u"weibliche Form",
    u"engl.": u"englisch",
    u"Hauptform": u"hauptsächlich benutzte Form'"
}

for line in sourcefile:
    if line[0] == "#":
        continue

    line = line.strip()
    if '"' in line:
        line = re.sub(';([^;"]+) "([^;"]+)"([^;]*);', ";\\1 \\2\\3;\\2\\3;", line)

    # speedup
    if speedvar != "":
        if speedvar in line:
            print(line)
            pass
        else:
            continue

    elements = line.split(";")

    for element in elements:
        if element == "":
            continue

        # wordcount += 1

        element = element.replace("&", "&amp;")
        element = element.replace("<", "&lt;")
        element = element.replace(">", "&gt;")
        element = element.replace("\"", "")
        translations = ""
        for i in elements:
            if i == "":
                continue
            if i != element:
                i = i.replace("&", "&amp;")
                i = i.replace("<", "&lt;")
                i = i.replace(">", "&gt;")
                i = i.replace("\"", "")
                for badWord in parentalControlWords:
                    if badWord in i:
                        i = '<span class="w" d:parental-control="1">' + i + u'</span><span class="sep" d:parental-control="1">; </span>'
                        break
                if '</span>' not in i:
                    i = '<span class="w">' + i + u'</span><span class="sep">; </span>'
                translations = translations + i

        # translations = translations[2:len(translations)]
        # translations = re.sub(r';</span>\s*$', "</span>", translations)
        translations = re.sub(r'(\([^);]+\))', '<i>\\1</i>', translations)
        translations = re.sub(r'> *<', u'> <', translations).strip()  # six-per-em space U+2006
        translations = re.sub(u'', '', translations)
        translations = re.sub(u'<span class="w">[  ]+<i>', u'<span><i>', translations).strip()

        for abbrev in abbreviations:
            if u'(' + abbrev in translations:
                translations = translations.replace(u'(' + abbrev, u'(<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>')
            if abbrev + u')' in translations:
                translations = translations.replace(abbrev + u')', u'<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>)')
            if abbrev + u', ' in translations:
                translations = translations.replace(abbrev + u', ', u'<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>, ')

        id = re.sub(r'(?u)[\"<>, ]', '_', element.lower())
        id = re.sub(r"(?u)_+", "_", id)
        id = re.sub(r"(?u)(.)_$", "\\1", id)

        dvalue = re.sub(r'\([^)]+\)', " ", element).strip()
        dvalue = re.sub('  +', ' ', dvalue).strip()
        dvalue = dvalue[:127]

        if dvalue == "":
            dvalue = id[:127]

        if id in result:
            if translations.lower() not in result[id].lower():
                result[id] = result[id] + "\n<p>" + translations + "</p>"
        else:
            lengths[id] = len(id)
            result[id] = "<p>" + translations + "</p>"
            dvalues[id] = u'\n<d:index d:value="' + dvalue + u'" d:title="' + dvalue + u'"/>'
            titles[id] = element
            dvaluesplain[id] = dvalue
            parentals[id] = ""
            linkwords[id] = urllib.quote(re.sub(r'\([^)]+\)|{[^}]+}|\[[^\]]+\]', "", element).strip().encode("utf-8"))
            headlines[id] = re.sub(r'(\([^)]+\))', '<i>\\1</i>', element)
            headlines[id] = re.sub(r'> *<', u'> <', headlines[id]).strip()  # six-per-em space U+2006
            if dvalue in morphology:
                for x in morphology[dvalue].split(","):
                    if u'\n<d:index d:value="' + normalize(x.lower()) + u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                        if x.lower() > dvalue.lower():
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + x + u' → ' + dvalue + u'"/>'
                        else:
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + dvalue + u' ← ' + x + u'"/>'
                        # if x[:len(dvalue)].lower() == dvalue.lower():
                        #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                        # else:
                        #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'
            for badWord in parentalControlWords:
                if badWord in headlines[id]:
                    parentals[id] = ' d:parental-control="1"'
                    break

            for abbrev in abbreviations:
                if u'(' + abbrev in headlines[id]:
                    headlines[id] = headlines[id].replace(u'(' + abbrev, u'(<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>')
                if abbrev + u')' in headlines[id]:
                    headlines[id] = headlines[id].replace(abbrev + u')', u'<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>)')
                if abbrev + u', ' in headlines[id]:
                    headlines[id] = headlines[id].replace(abbrev + u', ', u'<span title="' + abbreviations[abbrev] + u'">' + abbrev + u'</span>, ')

        dvalueSplit = dvalue.split()
        for i in dvalueSplit:
            if len(i) > 1:
                devalueHyphenSplit = i.split("-")
                for j in range(1, len(devalueHyphenSplit)):
                    if len(devalueHyphenSplit[j]) > 1:
                        if u'\n<d:index d:value="' + normalize(devalueHyphenSplit[j].lower()) + u'"' not in normalize(dvalues[id].lower()):
                            if devalueHyphenSplit[j].lower() > dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="' + devalueHyphenSplit[j] + u'" d:title="' + devalueHyphenSplit[j] + u' → ' + dvalue + u'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="' + devalueHyphenSplit[j] + u'" d:title="' + dvalue + u' ← ' + devalueHyphenSplit[j] + u'"/>'
                            # dvalues[id] = dvalues[id] + '\n<d:index d:value="'+devalueHyphenSplit[j]+u'" d:title="'+devalueHyphenSplit[j]+u' ⇒ '+dvalue+u'"/>'
                        # if devalueHyphenSplit[j] in morphology:
                        #     for x in morphology[devalueHyphenSplit[j]].split(","):
                        #         if u'\n<d:index d:value="' + normalize(x.lower()) + u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                        #             if x.lower() > dvalue.lower():
                        #                 dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + x + u' → ' + dvalue + u'"/>'
                        #             else:
                        #                 dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + dvalue + u' ← ' + x + u'"/>'
                        #             # if x[:len(dvalue)].lower() == dvalue.lower():
                        #             #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                        #             # else:
                        #             #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'
                if '\n<d:index d:value="' + normalize(i.lower()) + '"' not in normalize(dvalues[id].lower()):
                    if i[0] != "-" and i[len(i) - 1] != "-":
                        if dvalue[:len(i)].lower() != i.lower():
                            if i.lower() > dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="' + i + u'" d:title="' + i + u' ⇒ ' + dvalue + u'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="' + i + u'" d:title="' + dvalue + u' ← ' + i + u'"/>'
                            # dvalues[id] = dvalues[id] + '\n<d:index d:value="'+i+u'" d:title="'+i+u' ⇒ '+dvalue+u'"/>'
                        # if i in morphology:
                        #     for x in morphology[i].split(","):
                        #         if u'\n<d:index d:value="' + normalize(x.lower()) + u'"' not in normalize(dvalues[id].lower()) and normalize(x.lower()) != normalize(dvalue.lower()):
                        #             if x.lower() > dvalue.lower():
                        #                 dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + x + u' → ' + dvalue + u'"/>'
                        #             else:
                        #                 dvalues[id] = dvalues[id] + '\n<d:index d:value="' + x + u'" d:title="' + dvalue + u' ← ' + x + u'"/>'
                        #             # if x[:len(dvalue)].lower() == dvalue.lower():
                        #             #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+u'"/>'
                        #             # else:
                        #             #     dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+u'"/>'


sourcefile.close()
lengths2 = copy.copy(lengths)

for id in lengths2:
    id2 = re.sub(r'(.+)(\(|\))', "\\1", id)

    if id != id2 and id2 in result and id in result:
        parental2 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id2]:
                parental2 = 'd:parental-control="1" '
                break
        parental1 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id]:
                parental1 = 'd:parental-control="1" '
                break

        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>', '') + ', <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if id in morphology and id in result:
        for x in morphology[id].split(","):
            if x != id and x in result:
                parental = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[x]:
                        parental = 'd:parental-control="1" '
                        break
                parental1 = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[id]:
                        parental1 = 'd:parental-control="1" '
                        break

                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental + 'href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>', '') + ', <a href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'

    id2 = re.sub(r'_*\([^)]+\)_*', "", id)
    id2 = re.sub(r'^(der|die|das|den|dem|des|an|am|sein|ein|etwas|[enmr]*)_[a-z]+_([a-z]+)$', "\\2", id2)
    id2 = re.sub(r'(_|^)(jemand[ensr]*|eigen[res]*|der|die|das|dem|den|des[sen]*|vo[nm]|ein[ermns]*)(_|$)', "", id2)
    id2 = re.sub(r'^(in|im|ein|wo|an|am|hat|hatte|er|sie|es|ich|du|es|ihm|ihr|sich|sein|wird|wurde|war|sich|alle[nrs]*|nicht|kein[er]*|ohne|mit|total)_', "", id2)
    id2 = re.sub('_([a-z]*lassen$|w[eu]rden|ge[a-z]+|können|er[a-z]+|[a-z]+en)$', "", id2)

    if id != id2 and id2 in result and id in result:
        parental2 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id2]:
                parental2 = 'd:parental-control="1" '
                break
        parental1 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id]:
                parental1 = 'd:parental-control="1" '
                break

        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>', '') + ', <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if id in morphology and id in result:
        for x in morphology[id].split(","):
            if x != id and x in result:
                parental = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[x]:
                        parental = 'd:parental-control="1" '
                        break
                parental1 = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[id]:
                        parental1 = 'd:parental-control="1" '
                        break

                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental + 'href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>', '') + ', <a ' + parental + 'href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'

    id2 = re.sub(r'_*\([^)]+\)_*', "", id)
    id2 = re.sub(r'^[a-z]+_([a-z]+)$', "\\1", id2)

    if id != id2 and id2 in result and id in result:
        parental2 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id2]:
                parental2 = 'd:parental-control="1" '
                break
        parental1 = ""
        for badWord in parentalControlWords:
            if badWord in headlines[id]:
                parental1 = 'd:parental-control="1" '
                break

        if "<b>Siehe auch:</b>" not in result[id]:
            result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a>' not in result[id]:
                result[id] = result[id].replace('</div>', '') + ', <a ' + parental2 + 'href="x-dictionary:d:' + dvaluesplain[id2] + '">' + headlines[id2] + '</a></div>'
        if "<b>Siehe auch:</b>" not in result[id2]:
            result[id2] = result[id2] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
        else:
            if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[id2]:
                result[id2] = result[id2].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
    if id in morphology and id in result:
        for x in morphology[id].split(","):
            if x != id and x in result:
                parental = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[x]:
                        parental = 'd:parental-control="1" '
                        break
                parental1 = ""
                for badWord in parentalControlWords:
                    if badWord in headlines[id]:
                        parental1 = 'd:parental-control="1" '
                        break

                if "<b>Siehe auch:</b>" not in result[id]:
                    result[id] = result[id] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental + 'href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a>' not in result[id]:
                        result[id] = result[id].replace('</div>', '') + ', <a ' + parental + 'href="x-dictionary:d:' + dvaluesplain[x] + '">' + headlines[x] + '</a></div>'
                if "<b>Siehe auch:</b>" not in result[x]:
                    result[x] = result[x] + u'<div class="seealso"><b>Siehe auch:</b> <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'
                else:
                    if ' href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a>' not in result[x]:
                        result[x] = result[x].replace('</div>', '') + ', <a ' + parental1 + 'href="x-dictionary:d:' + dvaluesplain[id] + '">' + headlines[id] + '</a></div>'


print("\nXML-Datei wird erzeugt ...")
destfile = codecs.open('ThesaurusDeutsch.xml', 'w', 'utf-8')
destfile.write("""<?xml version="1.0" encoding="utf-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">""")

for id in lengths:
    wordcount += 1
    destfile.write(re.sub("  +", "", u"""
<d:entry id="%s" class="d" d:title="%s"%s>%s
<h2 d:pr="1">%s</h2>
%s
<div class="c" d:priority="2"><span><a href="https://www.openthesaurus.de/synonyme/%s">Aus OpenThesaurus.de</a> · © %s Daniel Naber</span></div>
</d:entry>
""" % (id, titles[id], parentals[id], dvalues[id], headlines[id], result[id], linkwords[id], downloadfileyear)))

destfile.write(u"""
<d:entry id="front_back_matter" d:title="Vorderer/hinterer Teil">
    <h1><b>OpenThesaurus Deutsch</b></h1>
    <div><small><b>Version: %s</b></small></div>
    <p>
        Dieser Thesaurus basiert auf dem Online-Thesaurus:<br/>
        <a href="https://www.openthesaurus.de">www.openthesaurus.de</a> von Daniel Naber. (Stand: %s, %s Einträge)
    </p>
    <p>
        <a href="https://tekl.de/dictversion.php?version=%s&amp;plugin=OpenThesaurus%%20Deutsch"><button>↺ Nach Update suchen</button></a>
    </p>
    <h3>Informationen und Hilfe</h3>
    <p>
        <ul>
            <li><a href="https://tekl.de/lexikon-plug-ins">Weitere Lexikon-Plug-ins für macOS</a></li>
            <li><a href="https://tekl.de/lexikon-tipps">Allgemeine Tipps zur Lexikon-App</a></li>
            <li><a href="https://tekl.de/lexikon-faq">Häufig gestellte Fragen und Hilfe bei Problemen</a></li>
            <li>Support erhalten Sie auf <a href="https://github.com/Tekl/openthesaurus-deutsch/issues">GitHub</a> (Issues) oder via <a href="mailto:support@tekl.de">support@tekl.de</a></li>
        </ul>
    </p>
    <h3>Über OpenThesaurus Deutsch</h3>
    <p>
        Das Python-Skript zur Umwandlung der OpenThesaurus-Wortliste in ein Lexikon-Plug-in wurde von Wolfgang Reszel entwickelt. Den Quellcode finden Sie auf <a href="https://github.com/Tekl/openthesaurus-deutsch">GitHub</a>.
    </p>
    <p>
        Die Wortformen-Datei, durch welche auch die Suche nach Wörtern im Plural möglich ist, wurde auf Basis des <a href="http://www.danielnaber.de/morphologie/">Morphologie-Lexikons</a> von Daniel Naber erstellt.
    </p>
    <p>
        <img src="Images/gplv3-88x31.png" align="left" style="padding-right:10px" alt=""/>
        <b>Lizenz:</b>
        Dieses Lexikon-Plug-in unterliegt der <a href="https://www.gnu.org/licenses/gpl.html">GPLv3</a><br/>
        Die Wortliste von OpenThesaurus unterliegt der
        <a href="https://creativecommons.org/licenses/LGPL/2.1/">CC-GNU LGPL</a><br/>
    </p>
</d:entry>
</d:dictionary>""" % (bundleVersion, downloadfiledate, wordcount, bundleVersion))
destfile.close()

print("\nHeruntergeladene Datei wird gelöscht ...")
os.system("rm openthesaurus.txt")
os.system("rm thesaurus.txt.zip")
os.system("rm LICENSE.txt")

print("\nVersionsnummern werden angepasst ...")

rtfFiles = ['installer/OpenThesaurus Deutsch.pkgproj', 'installer/finishup_de.rtfd/TXT.rtf', 'installer/finishup_en.rtfd/TXT.rtf', 'installer/intro_de.rtfd/TXT.rtf', 'installer/intro_en.rtfd/TXT.rtf', 'LIESMICH.md', 'README.md', 'Makefile']
for filename in rtfFiles:
    print(filename)
    if '.rtf' in filename:
        pmdocFile = codecs.open(filename, 'r', 'windows-1252')
    else:
        pmdocFile = codecs.open(filename, 'r', 'UTF-8')
    pmdoc = pmdocFile.read()
    pmdoc = re.sub(r"Version: .\d+.\d+.\d+(-beta)?", "Version: " + bundleVersion, pmdoc)
    pmdoc = re.sub(r">20\d+.\d+.\d+(-beta)?<", ">" + bundleVersion + "<", pmdoc)
    pmdoc = re.sub(r" 20\d+.\d+.\d+(-beta)?\"", " " + bundleVersion + "\"", pmdoc)
    pmdoc = re.sub(r" v20\d+.\d+.\d+(-beta)?", " v" + bundleVersion, pmdoc)
    if filename == 'Makefile':
        pmdoc = re.sub(r"([_ ])v20\d+.\d+.\d+(-beta)?", "\\1v" + bundleVersion + "", pmdoc)
        pmdoc = re.sub(r"/20\d+.\d+.\d+(-beta)?/", "/" + bundleVersion + "/", pmdoc)
    pmdoc = re.sub(r"20\d\d Wolfgang Reszel", datetime.datetime.today().strftime("%Y") + " Wolfgang Reszel", pmdoc)
    pmdocFile.close()
    if '.rtf' in filename:
        pmdocFile = codecs.open(filename, 'w', 'windows-1252')
    else:
        pmdocFile = codecs.open(filename, 'w', 'UTF-8')
    pmdocFile.write(pmdoc)
    pmdocFile.close()

print("Info.plist")
plistFile = codecs.open('Info.plist', 'r', 'UTF-8')
plist = plistFile.read()
plist = re.sub(r"(?u)(<key>CFBundleVersion</key>\s+<string>)[^<]+(</string>)", "\\g<1>" + bundleVersion + "\\2", plist)
plist = re.sub(r"(?u)(<key>CFBundleShortVersionString</key>\s+<string>)[^<]+(</string>)", "\\g<1>" + bundleVersion + "\\2", plist)
plist = re.sub(u"© \d\d\d\d ", u"© " + datetime.datetime.today().strftime("%Y") + u" ", plist)
plist = re.sub(u"© (\d\d\d\d)-\d\d\d\d ", u"© \\1-" + datetime.datetime.today().strftime("%Y") + u" ", plist)
plist = re.sub(r"version=\d\d\d\d\.\d+\.\d+(-beta)?", "version=" + bundleVersion, plist)
plist = re.sub(r" v\d\d\d\d\.\d+\.\d+(-beta)?", " v" + bundleVersion, plist)
plistFile.close()
plistFile = codecs.open('Info.plist', 'w', 'UTF-8')
plistFile.write(plist)
plistFile.close()

print("\nXML-Datei wird ausgewertet (Making) ... [" + speedvar + "]\n-----------------------------------------------------")
