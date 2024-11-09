# Changelog für OpenThesaurus Deutsch

Sorry, there’s no english changelog.

## v2024.11.09

### Geändert (Changed)

- Datenbestand vom 08.11.2024 mit 170954 Einträgen.

## v2024.07.15

### Geändert (Changed)

- Datenbestand vom 14.07.2024 mit 169339 Einträgen.

## v2024.07.14

### Geändert (Changed)

- Datenbestand vom 13.07.2024 mit 169335 Einträgen.

## v2024.05.14

### Geändert (Changed)

- Datenbestand vom 12.05.2024 mit 168769 Einträgen.

## v2023.12.28

### Geändert (Changed)

- Datenbestand vom 27.12.2023 mit 167367 Einträgen.
- Font-Auswahl reduziert, da das Lexikon schon länger nur noch System-Fonts unterstützt.

### Fehler behoben (Fixed)

- Automatische Aktivierung des Plug-ins nach der Installation verbessert. Manchmal wurden bereits aktivierte Plug-ins deaktiviert.

## v2022.07.02

### Geändert (Changed)

- Datenbestand vom 1.8.2022 mit 162012 Einträgen.

## v2022.07.22

### Geändert (Changed)

- Datenbestand vom 21.7.2022 mit 161844 Einträgen.
- Änderung des Namens im Copyright und im Klappentext (Wolfgang Reszel→Wolfgang Kreutz). 

## v2022.02.17

### Geändert (Changed)

- Datenbestand vom 16.02.2022 mit 159697 Einträgen.
- Code auf Python 3 aktualisiert, weil Python 2 mit macOS 12.3 nicht mehr verfügbar ist. Das ist aber nur relevant, wenn man das Plug-in selbst erzeugen möchte. 

## v2021.12.09

### Fehler behoben (Fixed)

- Der Installer behebt jetzt zuverlässiger das Problem mit leeren Seiten nach dem Update von einer sehr alten Version des Plug-ins.

### Geändert (Changed)

- Aktualisierte Plug-in-Grafik im Installer und fürs Bundle.
- Datenbestand vom 8.12.2021 mit 158487 Einträgen.

## 2021.11.05

### Fehler behoben (Fixed)

- Der Installer kann nun auch auf ganz frischen Systemen das Plug-in automatisch aktivieren.
- Der Installer verlangt nicht mehr, dass der Prozess DictionaryServiceHelper geschlossen sein muss. Ist nicht nötig.

### Geändert (Changed)

- Datenbestand vom 04.11.2021 mit 157761 Einträgen.

## v2021.10.17

### Fehler behoben (Fixed)

- Die Installation funktioniert nun wieder unter OS X 10.11 und bricht nicht mehr mit dem Fehler „Ungültige Signatur“ ab.

### Geändert (Changed)

- Datenbestand vom 16.10.2021 mit 157326 Einträgen.

## v2021.10.06

### Geändert (Changed)

- Das Installationsprogramm setzt nun die Standard-Einstellungen, sofern entsprechende Einträge in der Preferences-Datei fehlen. Damit wird verhindert, dass das Plug-in keine Inhalte zeigt ([siehe FAQ](https://tekl.de/lexikon-faq/lexikon-plug-zeigt-keine-inhalte)) falls die zuvor installierte Version weniger Einstellmöglichkeiten bot.
- Datenbestand vom 5.10.2021 mit 157093 Einträgen.

## v2021.09.29

### Fehler behoben (Fixed)

- Die Update-Funktion in den Einstellungen lieferte die falsche Versionsnummer und meinte, die aktuelle Version sei bereits veraltet. (Danke maelcum [#2](https://github.com/Tekl/beolingus-deutsch-englisch/issues/2))

### Geändert (Changed)

- Datenbestand vom 28.09.2021 mit 156873  Einträgen.

## v2021.09.27

### Hinzugefügt (Added)

- Man kann neben der Standardschrift von macOS aus 28 weiteren Fonts auswählen. Die Auswahl enthält größtenteils System-Fonts aber auch meine zwei kommerziellen Lieblings-Fonts „Sys 2.0“ und „PragmataPro“ von [Fabrizio Shiavi](https://fsd.it).
- In den Einstellungen des Plug-ins und im Klappentext (Vorderer/hinterer Teil) gibt es einen Button, über den Sie prüfen können, ob eine neue Version des Plug-ins vorliegt. Im Sinne der Datensparsamkeit erfolgt die Überprüfung nicht automatisch im Hintergrund, sondern nur manuell per Klick.
- Respektiert die [Jugendschutz-Einstellung](https://support.apple.com/de-de/guide/mac-help/mchlbcf0dfe2/mac) von macOS für anstößige Sprache. Damit lassen sich alle obszönen Einträge verbergen, die mit (vulg.) und (derb) gekennzeichnet sind.
- Verweilt der Mauspfeil auf Abkürzungen in Klammern wie [fig.], erscheint ein Tooltip mit einer Erläuterung.

### Geändert (Changed)

- Berücksichtigt deutlich mehr Wortformen bei Suchbegriffen (auf Basis des [Morphologie-Lexikons](https://www.danielnaber.de/morphologie/) von Daniel Naber, Stand 25.6.2021, LT v5.4)
- Das Plug-in liegt nun in einem moderneren Format vor, das allerdings nur zu OS X 10.11 und höher kompatibel ist. Das verhindert auf aktuellen Systemen willkürliche Abstürze bei einigen Programmen wie PDF Expert.
- Datenbestand vom 26.09.2021 mit 156834 Einträgen.

## v2020.05.08

### Geändert (Changed)

- Datenbestand vom 07.05.2020 mit 143736 Einträgen.

## v2020.03.22

### Geändert (Changed)

- Datenbestand vom 21.03.2020 mit 142157 Einträgen.
- Überarbeite Readme-Dateien (Danke an @zeilen).
- `make` nutzt nun das korrekte Datum.
- Hinweis nach erfolgreichem `make`-Befehl um "sudo" ergänzt (erforderlich für die Installation).

## v2019.04.25

### Geändert (Changed)

- Das Installationsprogramm enthält nun eine Deinstallations-Routine.
- Datenbestand vom 24.04.2019 mit 136480 Einträgen.

#### Fehler behoben (Fixed)

- Das Lexikon flackert nun nicht mehr bei der Eingabe von Suchbegriffen im Darkmode von macOS 10.14 Mojave.

## v2019.04.15

### Geändert (Changed)

- Das Plug-in wird wieder über ein Installations-Paket für alle Benutzer installiert. Über „Ort für die Installation ändern“ lässt es sich weiterhin für einzelne Benutzer installieren.
- Datenbestand vom 14.04.2019 mit 136354 Einträgen.
- Update für macOS 10.14 Mojave mit Unterstützung des Darkmode.

### Entfernt (Removed)

- Da die Updateprüfung auf neueren Versionen von macOS nicht mehr funktioniert, habe ich sie entfernt. Sie funktionierte eh nicht zuverlässig.
- Obsolete Einstellungen entfernt.

## v2018.05.23

### Geändert (Changed)

- Datenbestand vom 22.5.2018 mit 131901 Einträgen.
- Der im Plug-in integrierte Update-Check geschieht ab v2018.05.23 über HTTPS.
