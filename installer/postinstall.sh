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
	do shell script "pkill -KILL com.apple.DictionaryServiceHelper"
end try

tell application id "com.apple.installer"
	activate
	if user locale of (get system info) begins with "de_" then
		display dialog "Unter Umständen werden Sie gleich gefragt, ob das Installationsprogramm „System Events“ steuern darf. Dies ist erforderlich, um die Einstellungsdateien (Preferences) des Lexikons zu bearbeiten und das Plug-in automatisch zu aktivieren." & return & return & "Wenn Sie dem nicht trauen, können Sie auf „Nicht erlauben“ klicken. Dann müssen Sie das Plug-in selbst in den Einstellungen des Lexikon-Programms aktivieren." buttons {"Verstanden"} default button 1 giving up after 60 with icon caution
	else
		display dialog "Possibly the Installer asks for the permission to control “System Events”. This is necessary to edit the Preferences of the Dictionary App and automatically activate the Plugin." & return & return & "If you don’t trust this, you can click on “Don’t Allow”. Then you have to activate the Plugin in the Dictionary settings by yourself." buttons {"OK"} default button 1 giving up after 60 with icon caution
	end if
end tell

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

try
	if BundlePath begins with homeDir then set BundlePath to homeDir & "/Library/Containers/com.apple.Dictionary/Data/" & characters (length of homeDir) thru -1 of BundlePath
	tell application "System Events"
		try
			set locationToPlist to homeDir & "/Library/Preferences/com.apple.DictionaryServices.plist"
			set propList to property list file locationToPlist
		on error
			set locationToPlist to homeDir & "/Library/Containers/com.apple.Dictionary/Data/Library/Preferences/com.apple.DictionaryServices.plist"
			set propList to property list file locationToPlist
		end try
		
		set propList to property list file locationToPlist
		
		-- activate plugin
		if not (exists property list item "DCSActiveDictionaries" of propList) then
			make new property list item at end of propList with properties {kind:list, name:"DCSActiveDictionaries"}
		end if
		try
			set dicNode to property list item "DCSActiveDictionaries" of propList
			set pathFound to false
			repeat with i from 1 to (count of dicNode)
				set targetItem2 to item i of dicNode
				
				if value of targetItem2 contains BundlePath then
					set pathFound to true
					exit repeat
				end if
			end repeat
			if pathFound is false then
				make new property list item at end of dicNode with properties {kind:string, value:BundlePath}
			end if
		end try
		
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
end try

do shell script "killall cfprefsd"
EOF

rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryApp"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryManager"
rm -d -f -R "${HOME}/Library/Caches/com.apple.Dictionary"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryServices"

if [ -n "${COMMAND_LINE_INSTALL}" ]
	then exit 0
fi
