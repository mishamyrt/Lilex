VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

BUNDLE_DIR = bundle
BUILD_DIR = build
REPORTS_DIR = reports
GLYPHS_FILE = Lilex.glyphs

OS := $(shell uname)

define build-font
	$(VENV) python scripts/lilex.py build $(1)
endef

define check-font
	$(VENV) fontbakery check-googlefonts \
		--auto-jobs \
		--full-lists \
		--html "$(REPORTS_DIR)/universal_$(1).html" \
		"$(BUILD_DIR)/$(1)/"*
endef

configure: requirements.txt
	rm -rf $(VENV_DIR)
	make $(VENV_DIR)

configure-preview: preview/*.yaml preview/*.json
	cd preview; pnpm install

.PHONY: print-updates
print-updates:
	$(VENV) pip list --outdated
	cd preview; pnpm outdated

.PHONY: check
check:
	make clean-reports
	mkdir "$(REPORTS_DIR)"
	$(call check-font,"ttf")
	$(call check-font,"variable")

.PHONY: lint
lint:
	$(VENV) ruff scripts/
	$(VENV) pylint scripts/
	cd preview; pnpm eslint 'src/**/*.{svlete,ts}'

.PHONY: preview
preview:
	$(VENV) python scripts/show.py

.PHONY: generate
generate:
	$(VENV) python scripts/lilex.py generate

.PHONY: build
build:
	make clean-build
	$(call build-font)

.PHONY: build-preview
build-preview:
	cd preview; pnpm run build

.PHONY: run-preview
run-preview:
	cd preview; pnpm run dev

.PHONY: pack-bundle
pack-bundle:
	rm -rf "$(BUNDLE_DIR)"
	mkdir "$(BUNDLE_DIR)"
# Copy fonts
	cp -r "$(BUILD_DIR)/"* "$(BUNDLE_DIR)/"
# Copy reports
	cp "$(REPORTS_DIR)/"* "$(BUNDLE_DIR)/"
	cd "$(BUNDLE_DIR)"; zip -r Lilex.zip ./*

.PHONY: bundle
bundle:
	make build
	make check
	make pack-bundle

.PHONY: clean
clean:
	make clean-build
	make clean-reports

.PHONY: clean-build
clean-build:
	rm -rf "$(BUILD_DIR)"

.PHONY: clean-reports
clean-reports:
	rm -rf "$(REPORTS_DIR)"

.PHONY: ttf
ttf:
	$(call build-font,ttf)

.PHONY: otf
otf:
	$(call build-font,otf)

.PHONY: variable
variable:
	$(call build-font,variable)

install:
	make install-$(OS)

install-Darwin:
	rm -rf ~/Library/Fonts/Lilex
	cp -r build/variable ~/Library/Fonts/Lilex

install-Linux:
	rm -rf ~/.fonts/Lilex
	cp -r build/ttf ~/.fonts/Lilex

$(VENV_DIR): requirements.txt
	rm -rf "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	$(VENV) pip install wheel
	$(VENV) pip install -r requirements.txt
