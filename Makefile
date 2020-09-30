BUILD_DIRECTORY := "build"
GLYPHS_FILE := "Lilex.glyphs"
VF_FILE := "$(BUILD_DIRECTORY)/variable_ttf/Lilex-VF.ttf"
UNAME := $(shell uname)
ifeq (, $(shell which lsb_release))
OS := "$(UNAME)"
else
OS := "$(shell lsb_release -si)"
endif

all: ttf otf variable_ttf

ttf: raw_ttf
	$(foreach file,$(wildcard $(BUILD_DIRECTORY)/ttf/*.ttf),$(call ttf_fix,$(file)))

raw_ttf:
	fontmake -g $(GLYPHS_FILE) -o ttf \
	--output-dir "$(BUILD_DIRECTORY)/ttf" -i

otf:
	fontmake -g $(GLYPHS_FILE) -o otf \
	--output-dir "$(BUILD_DIRECTORY)/otf" -i

variable_ttf:
	fontmake -g $(GLYPHS_FILE) -o variable \
		--output-dir "$(BUILD_DIRECTORY)/variable_ttf"
	gftools fix-vf-meta $(VF_FILE)
	gftools fix-nonhinting $(VF_FILE) $(VF_FILE)
	gftools fix-gasp --autofix $(VF_FILE)
	gftools fix-dsig --autofix $(VF_FILE)
	rm $(BUILD_DIRECTORY)/variable_ttf/Lilex-VF-backup-fonttools-prep-gasp.ttf
	rm $(BUILD_DIRECTORY)/variable_ttf/Lilex-VF.ttf.fix

install:
	make install_$(UNAME)

bootstrap:
	make bootstrap_$(OS)

install_Darwin:
	rm -rf ~/Library/Fonts/Lilex
	cp -r build/otf ~/Library/Fonts/Lilex

bootstrap_Darwin:
	brew install cairo freetype harfbuzz pkg-config ttfautohint python3
	make bootstrap_pip

bootstrap_Ubuntu:
	sudo apt install python3-setuptools ttfautohint build-essential libffi-dev python-dev libgit2
	sudo make bootstrap_pip

bootstrap_pip:
	pip3 install fonttools git+https://github.com/googlefonts/gftools fontmake
	pip3 install -U cu2qu

install_Linux:
	mkdir -p ~/.fonts
	rm -rf ~/.fonts/Lilex

define ttf_fix
	gftools fix-dsig --autofix $(1)
	ttfautohint -I $(1) $(1)-hinted --stem-width-mode nnn --composites --windows-compatibility
	mv $(1)-hinted $(1)

endef
