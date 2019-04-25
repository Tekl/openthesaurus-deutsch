#!/bin/sh
osascript <<EOF
set installDir to "${2}"
set homeDir to "${HOME}"
set pluginName to "OpenThesaurus Deutsch.dictionary"

try
	tell application "System Events" to set dictPanelID to unix id of process "DictionaryPanel"
	do shell script "kill -s QUIT " & dictPanelID
end try
try
	tell application "System Events" to set dictPanelID to unix id of process "com.apple.DictionaryServiceHelp"
	do shell script "kill -s QUIT " & dictPanelID
end try

try
    do shell script "rm -rf " & quoted form of (homeDir & "/Library/Dictionaries/" & pluginName)
end try
try 
    do shell script "rm -rf " & quoted form of (homeDir & "/Library/Containers/com.apple.Dictionary/Data/Library/Dictionaries/" & pluginName)
end try
try
    do shell script "rm -rf " & quoted form of ("/Library/Dictionaries/" & pluginName) with administrator privileges
end try
try
    do shell script "/usr/sbin/pkgutil --forget de.tekl.dictionary.openThesaurusDeutsch" with administrator privileges
end try
try
    do shell script "/usr/sbin/pkgutil --forget de.tekl.dictionary.openThesaurusDeutsch.uninstall" with administrator privileges
end try
EOF

rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryApp"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryManager"
rm -d -f -R "${HOME}/Library/Caches/com.apple.Dictionary"
rm -d -f -R "${HOME}/Library/Caches/com.apple.DictionaryServices"

if [ -n "${COMMAND_LINE_INSTALL}" ]
	then exit 0
fi