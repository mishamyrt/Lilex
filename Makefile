# Project directories
BUILD_DIR := build
REPORTS_DIR := reports
SCRIPTS_DIR := scripts
SOURCES_DIR := sources
PYTHON_VERSION := 3.13

# Font sources
LILEX_ROMAN_SOURCE = $(SOURCES_DIR)/Lilex.glyphs
LILEX_ITALIC_SOURCE = $(SOURCES_DIR)/Lilex-Italic.glyphs

# Internal build variables
OS := $(shell uname)
VENV_DIR = ./.venv
VENV = . $(VENV_DIR)/bin/activate;

define check-static-dir
	$(VENV) fontbakery check-$(2) \
		--auto-jobs \
		--full-lists \
		-x opentype/STAT/ital_axis \
		-x fontdata_namecheck \
		--html "$(REPORTS_DIR)/static_$(1).html" \
		"$(BUILD_DIR)/$(1)/"*
endef

define check-variable-dir
	$(VENV) fontbakery check-$(2) \
		--auto-jobs \
		--full-lists \
		-x fontdata_namecheck \
		--html "$(REPORTS_DIR)/$(2)_$(1).html" \
		"$(BUILD_DIR)/$(1)/"*
endef

define check-ttf-file
	$(VENV) fontbakery check-$(2) \
		--auto-jobs \
		-x fontdata_namecheck \
		--html "$(REPORTS_DIR)/$(2)_$(1).html" \
		"$(BUILD_DIR)/ttf/Lilex-$(1).ttf"
endef

.PHONY: help
help: ## print this message
	@awk \
		'BEGIN {FS = ":.*?## "} \
		/^[a-zA-Z_-]+:.*?## / \
		{printf "\033[33m%-20s\033[0m %s\n", $$1, $$2}' \
		$(MAKEFILE_LIST)

.PHONY: configure
configure: ## setup build environment
	@rm -rf "$(VENV_DIR)"
	@uv venv --python $(PYTHON_VERSION)
	@uv sync
	@uv run youseedee A > /dev/null
	uv tool run lefthook install

.PHONY: configure
configure-preview: ## setup preview environment
	@cd preview; pnpm install

.PHONY: print-updates
print-updates: ## print list of outdated packages
	@$(VENV) uv pip list --outdated
	@cd preview; pnpm outdated

.PHONY: check
check: clean-reports ## check font quality
	@$(call check-static-dir,"ttf","googlefonts")
	@$(call check-variable-dir,"variable","googlefonts")

.PHONY: check-sequential
check-sequential: clean-reports ## check each font file quality
	@$(call check-ttf-file,"Bold","googlefonts")
	@$(call check-ttf-file,"ExtraLight","googlefonts")
	@$(call check-ttf-file,"Medium","googlefonts")
	@$(call check-ttf-file,"Regular","googlefonts")
	@$(call check-ttf-file,"Thin","googlefonts")
	@$(call check-variable-dir,"variable","googlefonts")
		
.PHONY: lint-py
format-py: ## check font builder code quality
	uv tool run ruff check --fix $(SCRIPTS_DIR)/

.PHONY: format-preview
format-preview: ## check preview website code quality
	cd preview; pnpm format

.PHONY: preview-env
preview-env:
	@$(VENV) python $(SCRIPTS_DIR)/preview_env.py generate fonts/ttf/Lilex-Regular.ttf preview/.env

.PHONY: preview
preview: preview-env ## run the preview
	cd preview; pnpm run dev

.PHONY: build-preview
build-preview: preview-env ## build the preview
	cd preview; pnpm run build

.PHONY: show
show: ## show CLI special symbols preview
	@$(VENV) python $(SCRIPTS_DIR)/show.py

.PHONY: generate
generate: ## regenerate the font sources with classes and features
	@$(VENV) python $(SCRIPTS_DIR)/generate.py \
		--config "sources/lilexgen_config.yaml" \
		generate

.PHONY: build
build: ## build the font
	@make clean-build
	@$(VENV) cd sources; gftools builder config.yaml

.PHONY: release
release: ## release the font
	@make build
	@rm -rf fonts
	@cp -r build fonts

.PHONY: release-notes
release-notes:
	@mkdir -p ./$(BUILD_DIR)
	$(VENV) python ./scripts/changelog.py notes Next > "./$(BUILD_DIR)/release-notes.md"

.PHONY: clean
clean: ## clean up
	@make clean-build
	@make clean-reports

.PHONY: clean-build
clean-build: ## clean up build artifacts
	@rm -rf "$(BUILD_DIR)"

.PHONY: clean-reports
clean-reports: ## clean up reports
	@rm -rf "$(REPORTS_DIR)"
	@mkdir "$(REPORTS_DIR)"

.PHONY: variable
variable: ## build variable font
	$(call build-font,variable)

.PHONY: install
install: ## install font to system (macOS and Linux only)
	@make install-$(OS)

.PHONY: install-Darwin
install-Darwin:
	@rm -rf ~/Library/Fonts/Lilex
	@cp -r build/variable ~/Library/Fonts/Lilex

install-Linux:
	@rm -rf ~/.fonts/Lilex
	@cp -r build/ttf ~/.fonts/Lilex
