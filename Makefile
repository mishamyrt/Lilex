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
	$(VENV) python scripts/lilex.py build $(1)
endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

configure_preview: preview/*.yaml preview/*.json
	cd preview; pnpm install

.PHONY: check
check:
	fontbakery check-universal --auto-jobs --ghmarkdown fontbakery_report.md build/**/*

.PHONY: lint
lint:
	$(VENV) ruff scripts/
	$(VENV) pylint scripts/

.PHONY: preview
preview:
	$(VENV) python scripts/show.py

.PHONY: generate
generate:
	$(VENV) python scripts/lilex.py generate

.PHONY: build
build:
	$(call build_font)

.PHONY: build_preview
build_preview:
	cd preview; pnpm run build

.PHONY: run_preview
run_preview:
	cd preview; pnpm run dev

.PHONY: bundle
bundle:
	rm -rf "$(BUILD_DIR)"
	make build
	cd "$(BUILD_DIR)"; zip -r Lilex.zip ./*

.PHONY: ttf
ttf:
	$(call build_font,ttf)

.PHONY: otf
otf:
	$(call build_font,otf)

.PHONY: variable
variable:
	$(call build_font,variable)

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
	$(VENV) pip install wheel
	$(VENV) pip install -r requirements.txt
