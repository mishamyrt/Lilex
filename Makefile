VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

BUILD_DIR = build
GLYPHS_FILE = Lilex.glyphs
REPORT_PREFIX = fontbakery_report_

OS := $(shell uname)

define build_font
	$(VENV) python scripts/lilex.py build $(1)
endef

define check_font
	$(VENV) fontbakery check-universal \
		--auto-jobs \
		--ghmarkdown "$(REPORT_PREFIX)$(1).md" \
		"$(BUILD_DIR)/$(1)/"* || true
endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

configure_preview: preview/*.yaml preview/*.json
	cd preview; pnpm install

.PHONY: check
check:
	$(call check_font,"ttf")
	$(call check_font,"variable")

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
	make clean
	make build
	cd "$(BUILD_DIR)"; zip -r Lilex.zip ./*

.PHONY: clean
clean:
	rm -f "$(REPORT_PREFIX)"*.md
	rm -rf "$(BUILD_DIR)"

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
	cp -r build/ttf ~/Library/Fonts/Lilex

install_Linux:
	rm -rf ~/.fonts/Lilex
	cp -r build/ttf ~/.fonts/Lilex

$(VENV_DIR): requirements.txt
	rm -rf "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	$(VENV) pip install wheel
	$(VENV) pip install -r requirements.txt
