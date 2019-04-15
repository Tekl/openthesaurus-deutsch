#!/bin/sh
osascript <<EOF
set installDir to "${2}"
set homeDir to "${HOME}"
set BundlePath to installDir & "/Library/Dictionaries/OpenThesaurus Deutsch.dictionary"
if BundlePath begins with "//" then set BundlePath to characters 2 thru -1 of BundlePath as string

try
	tell application "System Events" to set dictPanelID to unix id of process "DictionaryPanel"
	do shell script "kill -s QUIT " & dictPanelID
end try
try
	tell application "System Events" to set dictPanelID to unix id of process "com.apple.DictionaryServiceHelp"
	do shell script "kill -s QUIT " & dictPanelID
end try

try
	set locationToPlist to homeDir & "/Library/Preferences/com.apple.Dictionary.plist"

	tell application "System Events"
		set propList to property list file locationToPlist
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
	set locationToPlist to homeDir & "/Library/Preferences/com.apple.DictionaryServices.plist"

	tell application "System Events"
		try
			set dictPanelID to unix id of process "DictionaryPanel"
			do shell script "kill -s QUIT " & dictPanelID
		end try
		try
			set dictPanelID to unix id of process "com.apple.DictionaryServiceHelp"
			do shell script "kill -s QUIT " & dictPanelID
		end try
		set propList to property list file locationToPlist
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