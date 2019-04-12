###########################
# Makefile
#
#
#

###########################

# You need to edit these values.

OS_VERSION = `sw_vers -productVersion | sed 's/\(^....\).*/\1.x/'`
OS_VERSION2 = `sw_vers -productVersion | sed 's/\(^....\).*/\1.0/'`

DICT_NAME       = OpenThesaurus Deutsch
DICT_NAME_NSPC  = OpenThesaurus_Deutsch
DICT_SRC_PATH   = ThesaurusDeutsch.xml
CSS_PATH        = ThesaurusDeutsch.css
PMDOC_NAME      = ThesaurusDeutsch.pmdoc
PLIST_PATH      = Info.plist
DATE            = `date +"v%Y.%m.%d"`
CURR_PATH       = `pwd`

DICT_BUILD_OPTS = -c 2 -t 1 -e 0 -v 10.6
#DICT_BUILD_OPTS = -c 2 -t 1 -e 0 -v 10.11

# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

DICT_BUILD_TOOL_DIR	    = /Developer/Auxiliary Tools/Dictionary\ Development\ Kit
#PACKAGE_MAKER_DIR       = /Developer/Auxiliary Tools/PackageMaker.app
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Developer/Utilities/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Applications/Auxiliary\ Tools/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Applications/Utilities/Dictionary\ Development\ Kit
endif
DICT_BUILD_TOOL_BIN	    = $(DICT_BUILD_TOOL_DIR)/bin

###########################

DICT_DEV_KIT_OBJ_DIR	=	./objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
RM			=	/bin/rm

CR = `echo "\r"`

###########################

all: xml fromxml

xml:
	@/usr/bin/python createxml.py $(OS_VERSION) $(OS_VERSION2)
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

fromxml:
	@$(DICT_BUILD_TOOL_BIN)/build_dict.sh $(DICT_BUILD_OPTS) "$(DICT_NAME)" $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	@mkdir "$(DICT_DEV_KIT_OBJ_DIR)/Dictionaries"
	@mv -f "$(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary" "$(DICT_DEV_KIT_OBJ_DIR)/Dictionaries/"
	@echo "Done."
	@echo "Use 'make install' to install the dictionary or 'make dmg' to create the Disk Image."
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

dmg:
	@echo "Creating Disk Image"
	@mkdir releases/2019.04.10 | true
	@/Applications/DMG\ Canvas.app/Contents/Resources/dmgcanvas $(DICT_NAME_NSPC).dmgCanvas releases/2019.04.10/$(DICT_NAME_NSPC).dmg -setTextString version v2019.04.10
	@open releases/2019.04.10/$(DICT_NAME_NSPC).dmg
	@echo "- use 'make notarize' to notarize the disk image"
	@echo "- use 'make nhistory' to check the notarization status"
	@echo "- use 'make nstaple' to include the notarization ticket into the disk image"
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null
	
signinstaller:
	xattr -rc Dictionary\ Installer.app
	codesign -f --deep --options=runtime --timestamp --entitlements Entitlements.plist -s 3D3Y3WDMYF -v Dictionary\ Installer.app

notarizeinstaller:
	xcrun altool --notarize-app --primary-bundle-id "de.tekl.dictionaryInstaller" --username "tekl@mac.com" --password "@keychain:AC_PASSWORD" --file ../Dictionary\ Installer/Dictionary\ Installer.app
	
notarize:
	xcrun altool --notarize-app --primary-bundle-id "de.tekl.dictionary.openThesaurusDeutsch.dmg" --username "tekl@mac.com" --password "@keychain:AC_PASSWORD" --file releases/2019.04.10/$(DICT_NAME_NSPC).dmg

nhistory:
	xcrun altool --notarization-history 0 -u "tekl@mac.com" -p "@keychain:AC_PASSWORD"

nstaple:
	xcrun stapler staple releases/2019.04.10/$(DICT_NAME_NSPC).dmg

install:
	@echo "Installing into $(DESTINATION_FOLDER)".
	@osascript -e 'tell application "Dictionary.app" to quit'
	@rm -rf ~/Library/Caches/com.apple.DictionaryApp
	@rm -rf ~/Library/Caches/com.apple.DictionaryManager
	@rm -rf ~/Library/Caches/com.apple.Dictionary
	@rm -rf ~/Library/Caches/com.apple.DictionaryServices
	@defaults write com.apple.Dictionary WebKitDeveloperExtras -bool true
	@mkdir -p $(DESTINATION_FOLDER)
	@ditto --noextattr --norsrc $(DICT_DEV_KIT_OBJ_DIR)/Dictionaries/"$(DICT_NAME)".dictionary $(DESTINATION_FOLDER)/"$(DICT_NAME)".dictionary
	@touch $(DESTINATION_FOLDER)
	@echo "Done."
	@open -a Dictionary
	@echo "To test the new dictionary, try Dictionary.app."
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

clean:
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)_leo
	$(RM) -f $(DICT_SRC_PATH)
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null
