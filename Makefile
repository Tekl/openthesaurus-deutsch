###########################
# Makefile
# for OpenThesaurus Deutsch v2024.05.14
# by Wolfgang Kreutz
# https://github.com/Tekl/openthesaurus-deutsch
###########################

# You need to edit these values.

OS_VERSION = `sw_vers -productVersion | sed 's/\(^....\).*/\1.x/'`
OS_VERSION2 = `sw_vers -productVersion | sed 's/\(^....\).*/\1.0/'`

DICT_NAME       = OpenThesaurus Deutsch
DICT_NAME_NSPC  = OpenThesaurus_Deutsch
DICT_SRC_PATH   = ThesaurusDeutsch.xml
CSS_PATH        = ThesaurusDeutsch.css
PLIST_PATH      = Info.plist
DATE            = `date +"%Y.%m.%d"`
CURR_PATH       = `pwd`
VERSION         = `cat VERSION`
VERSION_ZIP     = `cat ../../VERSION`

DICT_BUILD_OPTS = -c 2 -t 1 -e 0 -v 10.11

# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

DICT_BUILD_TOOL_DIR	    = /Developer/Auxiliary\ Tools/Dictionary\ Development\ Kit
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Developer/Utilities/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Applications/Auxiliary\ Tools/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Applications/Additional\ Tools/Utilities/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /DevTools/Utilities/Dictionary\ Development\ Kit
endif
ifeq ("$(wildcard $(DICT_BUILD_TOOL_DIR))","")
DICT_BUILD_TOOL_DIR	    = /Applications/Utilities/Dictionary\ Development\ Kit
endif
DICT_BUILD_TOOL_BIN	    = $(DICT_BUILD_TOOL_DIR)/bin

###########################

DICT_DEV_KIT_OBJ_DIR = ./objects
export DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER = /Library/Dictionaries
RM = /bin/rm

CR = `echo "\r"`

###########################

all: createxmlbeta build

release: createxml build

releasedist: createxml build releasedmg notarize

createxmlbeta:
	@echo $(DATE)-beta > VERSION
	@python3 createxml.py beta

createxml:
	@echo $(DATE) > VERSION
	@python3 createxml.py release

build:
	@$(DICT_BUILD_TOOL_BIN)/build_dict.sh $(DICT_BUILD_OPTS) "$(DICT_NAME)" "$(DICT_SRC_PATH)" "$(CSS_PATH)" "$(PLIST_PATH)"
	@mkdir "$(DICT_DEV_KIT_OBJ_DIR)/Dictionaries"
	@mkdir releases/$(VERSION)/ | true
	@Rez -a images/icons/dictplug.rsrc -o "$(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary/Icon"$$'\r'
	@SetFile -a C "$(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary"
	@SetFile -a V "$(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary/Icon"$$'\r'
	@mv -f "$(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary" "$(DICT_DEV_KIT_OBJ_DIR)/Dictionaries/"
	@cd $(DICT_DEV_KIT_OBJ_DIR)/Dictionaries; zip -r "../../releases/$(VERSION_ZIP)/${DICT_NAME_NSPC}_dictionaryfile.zip" "$(DICT_NAME).dictionary/"
	@echo "Done."
	@echo "Use 'sudo make install' to install the dictionary or 'make dmg' or 'make releasedmg' to create the Disk Image."
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

dmg:
	@echo "Creating Beta Installer ..."
	@mkdir releases/$(VERSION)/ | true
	@/usr/local/bin/packagesbuild --build-folder "$(shell pwd)/releases" "installer/$(DICT_NAME).pkgproj"
	@/usr/bin/productsign --sign "Developer ID Installer: Wolfgang Kreutz (3D3Y3WDMYF)" "$(shell pwd)/releases/$(DICT_NAME) Temp.pkg" "$(shell pwd)/releases/$(DICT_NAME) Installation.pkg"
	@rm "$(shell pwd)/releases/$(DICT_NAME) Temp.pkg"
	@echo "Creating Beta Disk Image …"
	@/Applications/DMG\ Canvas.app/Contents/Resources/dmgcanvas installer/$(DICT_NAME_NSPC).dmgCanvas releases/$(VERSION)/$(DICT_NAME_NSPC).dmg -setTextString version v$(VERSION)
	@echo "Beta Installer and Beta Disk Image created."
	@open releases/$(VERSION)/$(DICT_NAME_NSPC).dmg
	@echo "- use 'make notarize' to notarize and staple the disk image"
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

releasedmg:
	@echo "Creating Installer ..."
	@mkdir releases/$(VERSION)/ | true
	@/usr/local/bin/packagesbuild --build-folder "$(shell pwd)/releases" "installer/$(DICT_NAME).pkgproj"
	@/usr/bin/productsign --sign "Developer ID Installer: Wolfgang Kreutz (3D3Y3WDMYF)" "$(shell pwd)/releases/$(DICT_NAME) Temp.pkg" "$(shell pwd)/releases/$(DICT_NAME) Installation.pkg"
	@rm "$(shell pwd)/releases/$(DICT_NAME) Temp.pkg"
	@echo "Creating Disk Image …"
	@/Applications/DMG\ Canvas.app/Contents/Resources/dmgcanvas installer/$(DICT_NAME_NSPC).dmgCanvas releases/$(VERSION)/$(DICT_NAME_NSPC).dmg -setTextString version v$(VERSION)
	@echo "Installer and Disk Image created."
	@open releases/$(VERSION)/$(DICT_NAME_NSPC).dmg
	@echo "- use 'make notarize' to notarize and staple the disk image"
	@afplay /System/Library/Sounds/Purr.aiff > /dev/null

notarize:
	xcrun notarytool submit --keychain-profile 3D3Y3WDMYF --wait releases/$(VERSION)/$(DICT_NAME_NSPC).dmg
	xcrun stapler staple releases/$(VERSION)/$(DICT_NAME_NSPC).dmg

install:
	@echo "Installing into $(DESTINATION_FOLDER)".
	@osascript -e 'tell application "Dictionary.app" to quit'
	@rm -rf ~/Library/Caches/com.apple.DictionaryApp
	@rm -rf ~/Library/Caches/com.apple.DictionaryManager
	@rm -rf ~/Library/Caches/com.apple.Dictionary
	@rm -rf ~/Library/Caches/com.apple.DictionaryServices
	@rm -rf $(DESTINATION_FOLDER)/"$(DICT_NAME)".dictionary
	@defaults write com.apple.Dictionary WebKitDeveloperExtras -bool true
	@mkdir -p $(DESTINATION_FOLDER)
	@ditto --noextattr $(DICT_DEV_KIT_OBJ_DIR)/Dictionaries/"$(DICT_NAME)".dictionary $(DESTINATION_FOLDER)/"$(DICT_NAME)".dictionary
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
