VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

BUNDLE_DIR = bundle
BUILD_DIR = build
REPORTS_DIR = reports
GLYPHS_FILE = Lilex.glyphs

OS := $(shell uname)

define build_font
	$(VENV) python scripts/lilex.py build $(1)
endef

define check_font
	$(VENV) fontbakery check-universal \
		--auto-jobs \
		--ghmarkdown "$(REPORTS_DIR)/universal_$(1).md" \
		"$(BUILD_DIR)/$(1)/"*
endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

configure_preview: preview/*.yaml preview/*.json
	cd preview; pnpm install

.PHONY: check
check:
	make clean_reports
	mkdir "$(REPORTS_DIR)"
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
	make clean_build
	$(call build_font)

.PHONY: build_preview
build_preview:
	cd preview; pnpm run build

.PHONY: run_preview
run_preview:
	cd preview; pnpm run dev

.PHONY: bundle
bundle:
	make build
	make check
	rm -rf "$(BUNDLE_DIR)"
	mkdir "$(BUNDLE_DIR)"
# Copy fonts
	cp -r "$(BUILD_DIR)/"* "$(BUNDLE_DIR)/"
# Copy reports
	cp "$(REPORTS_DIR)/"* "$(BUNDLE_DIR)/"
	cd "$(BUNDLE_DIR)"; zip -r Lilex.zip ./*

.PHONY: clean
clean:
	make clean_build
	make clean_reports

.PHONY: clean_build
clean_build:
	rm -rf "$(BUILD_DIR)"

.PHONY: clean_reports
clean_reports:
	rm -rf "$(REPORTS_DIR)"

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
