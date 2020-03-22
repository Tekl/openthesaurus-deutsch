🇩🇪 [Deutsche Liesmich-Datei](LIESMICH.md)

## OpenThesaurus Deutsch Dictionary Plugin

_Version: 2020.03.16 - Mac OS X 10.6 to macOS 10.14_<br>
_Copyright © 2020 Wolfgang Reszel and Daniel Naber_

![Screenshot](images/screenshots/OpenThesaurus_Screen_1.png)

This plugin extends Apple's Dictionary Application with a **German thesaurus**.

The content of this plugin is based on the online thesaurus [www.openthesaurus.de](https://www.openthesaurus.de/) by Daniel Naber.

The Python script to convert the OpenThesaurus dictionary into a dictionary plugin was developed by Wolfgang Reszel.

**Updates and further informations:** [www.tekl.de](https://www.tekl.de).<br>
**Support and source code:** [github.com/Tekl/openthesaurus-deutsch](https://github.com/Tekl/openthesaurus-deutsch)<br>
**Changelog:** [CHANGELOG.md](https://github.com/Tekl/openthesaurus-deutsch/blob/master/CHANGELOG.md)<br>
**Donation:** [PayPal](https://www.paypal.me/WolfgangReszel) 

### Download

You can choose to either download the plain [Dictionary plugin bundle in a ZIP file (OpenThesaurus_Deutsch_dictionaryfile.zip)](https://github.com/Tekl/openthesaurus-deutsch/releases) to install manually, or a [disk image containing an installer package (OpenThesaurus_Deutsch.dmg)](https://github.com/Tekl/openthesaurus-deutsch/releases).

### Installation

#### Installer

1. Download the plugin installer: [OpenThesaurus_Deutsch.dmg](https://github.com/Tekl/openthesaurus-deutsch/releases)
2. Double-click on “OpenThesaurus Deutsch Installation” to start the installer.
3. Follow its instructions. To install the plugin for the current user and not for all users, click on “Change Install Location …” in the installer and select “Install for me only”.

#### Manual Installation for Mac OS X 10.7 or newer

1. Download the zipped dictionary plugin bundle: [OpenThesaurus Deutsch.dictionaryfile.zip](https://github.com/Tekl/openthesaurus-deutsch/releases)
2. Launch the application “Dictionary.app” und execute the command “Open dictionary folder” from the File menu.<br>
   ![Step 1](images/manual%20installation/dict-inst-1cursor.png)
3. The Finder will open a window with the folder “Dictionaries”. Drag and drop the unzipped plugin bundle into that Finder window.<br>
   ![Step 2](images/manual%20installation/dict-inst-2cursor.png)
4. Quit and restart the application “Dictionary.app”, so it will detect the newly installed plugin. Open the Preferences of “Dictionary.app” (⌘+Comma), scroll to the entry “OpenThesaurus Deutsch” and click the checkbox.<br>
   ![Step 3](images/manual%20installation/dict-inst-3cursor.png)

#### Manual Installation for Mac OS X 10.6

1. Download the zipped dictionary plugin bundle: [OpenThesaurus Deutsch.dictionaryfile.zip](https://github.com/Tekl/openthesaurus-deutsch/releases)
2. Drag and drop the unzipped plugin bundle into the folder `/Library/Dictionaries` (for all users) or `~/Library/Dictionaries` (for current user). Maybe you have to create the folder first.
3. Quit and restart the application “Dictionary.app”, so it will detect the newly installed plugin. Open the Preferences of “Dictionary.app” (⌘+Comma), scroll to the entry “OpenThesaurus Deutsch” and click the checkbox.
4. It could be necessary to re-login/restart or to quit the process “DictionaryPanel” in the Activity Monitor, so the plugin can be used in the dictionary panel (⌃⌘D).

### Uninstalling

You can also manually delete the plugin from the folder `/Library/Dictionaries` or `~/Library/Dictionaries` and restart the “Dictionary.app”.

### Licenses

- The word list from OpenThesaurus is licensed under [CC-GNU LGPL](https://creativecommons.org/licenses/LGPL/2.1/)

- This plugin and the build scripts are licensed under [GPLv3](https://www.gnu.org/licenses/gpl.html)<br><br>
  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.<br><br>
  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.<br><br>
  You should have received a copy of the [GNU General Public License](LICENSE) along with this program. If not, see <https://www.gnu.org/licenses/>.

