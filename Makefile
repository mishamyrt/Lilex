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
		-o "$(1)" \
		--output-dir "$(2)"
endef


define hint_ttf
	gftools fix-font "$(1)"
	rm "$(1)"
	mv "$(1).fix" "$(1)"

endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

regenerate:
	python3 generator/main.py

build: ttf otf variable_ttf

ttf:
	$(call build_font,ttf,$(TTF_DIR))
	$(VENV) $(foreach file,$(wildcard $(TTF_DIR)/*.ttf),$(call hint_ttf,$(file)))
	
otf:
	$(call build_font,otf,$(OTF_DIR))

variable_ttf:
	$(call build_font,variable,$(VTTF_DIR))
	gftools fix-font "$(VTTF_FILE)"
	rm "$(VTTF_FILE)"
	mv "$(VTTF_FILE).fix" "$(VTTF_FILE)"

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
