VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

BUILD_DIR = build
GLYPHS_FILE = Lilex.glyphs

OTF_DIR = $(BUILD_DIR)/otf
TTF_DIR = $(BUILD_DIR)/ttf
VTTF_DIR = $(BUILD_DIR)/variable_ttf
VTTF_FILE = $(VTTF_DIR)/Lilex-VF.ttf

OS := $(shell uname)

define build_font
	$(VENV) fontmake \
		-g $(GLYPHS_FILE) \
		-a \
		-o "$(1)" \
		--output-dir "$(2)"
endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

regenerate:
	python3 scripts/apply-features.py

build: ttf otf variable_ttf

bundle:
	rm -rf "$(BUILD_DIR)"
	make build
	cd "$(BUILD_DIR)"; zip -r Lilex.zip ./*

ttf:
	$(call build_font,ttf,$(TTF_DIR))

otf:
	$(call build_font,otf,$(OTF_DIR))

variable_ttf:
	$(call build_font,variable,$(VTTF_DIR))

install:
	make install_$(OS)

install_Darwin:
	rm -rf ~/Library/Fonts/Lilex
	cp -r build/otf ~/Library/Fonts/Lilex

install_Linux:
	mkdir -p ~/.fonts
	rm -rf ~/.fonts/Lilex

$(VENV_DIR): requirements.txt
	rm -rf "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	$(VENV) pip install -r requirements.txt
