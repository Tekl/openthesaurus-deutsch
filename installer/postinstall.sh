#!/bin/sh
osascript <<EOF
set installDir to "${2}"
set homeDir to "${HOME}"
set bundleID to "de.tekl.dictionary.openThesaurusDeutsch"
set BundlePath to installDir & "/Library/Dictionaries/OpenThesaurus Deutsch.dictionary"
if BundlePath begins with "//" then set BundlePath to characters 2 thru -1 of BundlePath as string

try
	do shell script "pkill DictionaryPanel"
end try
try
	do shell script "pkill Dictionary"
end try
try
	do shell script "pkill -KILL com.apple.DictionaryServiceHelper"
end try

tell application id "com.apple.installer"
	activate
	if (do shell script "defaults read -g AppleLocale") begins with "de_" then
		display dialog "Soll das das gerade installierte Plug-in automatisch aktiviert werden?" & return & return & "Falls ja, werden Sie im Anschluss gefragt, ob das Installationsprogramm „System Events“ steuern darf. Dies ist erforderlich, um die Einstellungsdatei (Preferences) des Lexikons entsprechend zu verändern." & return & return & "Wenn Sie dem nicht trauen, können Sie auf „Überspringen“ klicken. Dann müssen Sie das Plug-in in den Einstellungen des Lexikon-Programms selbst aktivieren." buttons {"Überspringen", "Plug-in aktivieren"} cancel button 1 default button 2 giving up after 60 with icon caution with title "Lexikon-Plug-in aktivieren?"
	else
		display dialog "Should the installed plugin be activated automatically?" & return & return & "If yes, you will then be asked whether the Installer is allowed to control “System Events”. This is necessary to make changes to the preferences file of the Dictionary." & return & return & "If you do not trust this, you can click on “Skip”. You must then activate the plug-in in the settings of the Dicrionary." buttons {"Skip", "Activate plugin"} cancel button 1 default button 2 giving up after 60 with icon caution with title "Activate Dictionary plugin?"
	end if
end tell

set allPaths to {}
try
	tell application "System Events"
		try
			set locationToPlist to homeDir & "/Library/Preferences/com.apple.Dictionary.plist"
			set propList to property list file locationToPlist
		on error
			set locationToPlist to homeDir & "/Library/Containers/com.apple.Dictionary/Data/Library/Preferences/com.apple.Dictionary.plist"
			set propList to property list file locationToPlist
		end try
		
		set dicNode to property list item "dictionaries" of property list item 0 of property list item "window settings" of propList
		set dicNodeItems to (every property list item of dicNode)
		
		set pathFound to false
		repeat with i from 1 to (count of dicNodeItems)
			set targetItem2 to item i of dicNodeItems
			set targetDisclosureOpenedList to (every property list item of targetItem2 whose name is equal to "disclosure opened")
			set targetPathList to (every property list item of targetItem2 whose name is equal to "path")
			repeat with i from 1 to (count of targetDisclosureOpenedList)
				set targetDisclosureOpened to item 1 of targetDisclosureOpenedList
			end repeat
			repeat with i from 1 to (count of targetPathList)
				set targetPath to item 1 of targetPathList
			end repeat
			set end of allPaths to value of targetPath
			
			if value of targetPath contains BundlePath then
				set pathFound to true
				set value of targetDisclosureOpened to true
				exit repeat
			end if
		end repeat
		
		if pathFound is false then
			set newItem to make new property list item at end of dicNode with properties {kind:record}
			make new property list item at end of newItem with properties {kind:boolean, name:"disclosure opened", value:true}
			make new property list item at end of newItem with properties {kind:string, name:"path", value:BundlePath}
			make new property list item at end of newItem with properties {kind:boolean, name:"user choice", value:true}
		end if
	end tell
end try

if BundlePath begins with homeDir then set BundlePath to homeDir & "/Library/Containers/com.apple.Dictionary/Data/" & characters (length of homeDir) thru -1 of BundlePath
tell application "System Events"
	do shell script "touch " & homeDir & "/Library/Preferences/com.apple.DictionaryServices.plist"
	set locationToPlist to homeDir & "/Library/Preferences/com.apple.DictionaryServices.plist"
	set propList to property list file locationToPlist
	
	-- activate plugin
	if not (exists property list item "DCSActiveDictionaries" of propList) then
		make new property list item at end of propList with properties {kind:list, name:"DCSActiveDictionaries"}
	end if
	
	set dicNode to property list item "DCSActiveDictionaries" of propList
	if (count of property list items of dicNode) is 0 then
		repeat with aPath in allPaths
			if aPath contains "/AssetsV2/" then
				set dictBID to value of property list item "CFBundleIdentifier" of property list file (aPath & "/Contents/Info.plist")
				make new property list item at end of dicNode with properties {kind:string, value:dictBID}
			else
				make new property list item at end of dicNode with properties {kind:string, value:aPath}
			end if
		end repeat
	end if
	set pathFound to false
	repeat with i from 1 to (count of property list items of dicNode)
		set targetItem2 to property list item i of dicNode
		
		if value of targetItem2 contains BundlePath then
			set pathFound to true
			exit repeat
		end if
	end repeat
	if pathFound is false then
		make new property list item at end of dicNode with properties {kind:string, value:BundlePath}
	end if
	
	-- set missing preferences to avoid blank page issues
	if not (exists property list item "DCSDictionaryPrefs" of propList) then
		make new property list item at end of propList with properties {kind:record, name:"DCSDictionaryPrefs"}
	end if
	try
		set dicPrefs to property list item bundleID of property list item "DCSDictionaryPrefs" of propList
	on error
		set dicPrefs to make new property list item at end of property list item "DCSDictionaryPrefs" of propList with properties {kind:record, name:bundleID}
	end try
	if not (exists property list item "Font" of dicPrefs) then
		make new property list item at end of dicPrefs with properties {kind:string, name:"Font", value:"0"}
	end if
	if not (exists property list item "ShowCopyright" of dicPrefs) then
		make new property list item at end of dicPrefs with properties {kind:string, name:"ShowCopyright", value:"1"}
	end if
end tell

-- defaults write is neccessary to update the preferences cache (killall does not work in all cases)
try
	do shell script "defaults read com.apple.DictionaryServices"
	do shell script "defaults write com.apple.DictionaryServices de.tekl.InstallDate \"$(date)\""
end try
do shell script "defaults read com.apple.Dictionary"
do shell script "defaults write com.apple.Dictionary de.tekl.InstallDate \"$(date)\""
do shell script "killall cfprefsd"
EOF

rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryApp"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryManager"
rm -d -f -R "${HOME}/Library/Caches/com.apple.Dictionary"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryServices"

if [ -n "${COMMAND_LINE_INSTALL}" ]
	then exit 0
fi
