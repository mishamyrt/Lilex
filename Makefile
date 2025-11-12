# Project directories
BUILD_DIR := build
RELEASE_DIR := fonts
REPORTS_DIR := reports
SCRIPTS_DIR := scripts
SOURCE_DIR := sources
WEBSITE_DIR := website

# Internal build variables
PYTHON_VERSION := 3.13
OS := $(shell uname)
VENV_DIR = ./.venv
VENV = . $(VENV_DIR)/bin/activate;

# Font build

.PHONY: configure
configure: ## setup font build environment
	@rm -rf "$(VENV_DIR)"
	@uv venv --python $(PYTHON_VERSION)
	@uv sync
	@uv run youseedee A > /dev/null
	uv tool run lefthook install

.PHONY: generate
generate: ## regenerate the font sources
	@$(VENV) python $(SCRIPTS_DIR)/generate.py \
		--config "$(SOURCE_DIR)/lilexgen_config.yaml" \
		generate

.PHONY: build
build: build-mono ## build the font

.PHONY: build-mono
build-mono: ## build Lilex monospaced font
	@$(call build-font,Lilex)

.PHONY: release
release: build ## release the font
	@rm -rf $(RELEASE_DIR)
	@cp -r $(BUILD_DIR) $(RELEASE_DIR)

define build-font
	@rm -rf $(BUILD_DIR)/$(1)
	@$(VENV) cd $(SOURCE_DIR)/$(1); gftools builder config.yaml
endef

# Font quality check

.PHONY: check
check: ## check Lilex font quality
	@make check-mono

.PHONY: check-mono 
check-mono: ## check Lilex font quality
	$(call fontbakery-check,parallel,Lilex)

.PHONY: check-sequential
check-sequential: ## check Lilex font quality sequentially (for CI)
	$(call fontbakery-check,sequential,Lilex)

define fontbakery-check
	$(call fontbakery-check-format,$(1),$(2),variable)
	$(call fontbakery-check-format,$(1),$(2),ttf)
endef

# usage: $(call fontbakery-check,[parallel|sequential],font_name,font_format)
define fontbakery-check-format
	@mkdir -p "$(REPORTS_DIR)"
	@$(VENV) fontbakery check-googlefonts \
		$(if $(filter-out parallel,$(1)),--auto-jobs) \
		-x fontdata_namecheck \
		--html "$(REPORTS_DIR)/$(2)_$(3).html" \
		"$(BUILD_DIR)/$(2)/$(3)/"*
endef

# Scripts and scripts management

.PHONY: print-updates
scripts-print-updates: ## print list of outdated packages
	@uv tree --depth 1 --outdated

.PHONY: scripts-lint
scripts-lint: ## lint scripts
	@uv tool run ruff check $(SCRIPTS_DIR)/

.PHONY: scripts-format
scripts-format: ## format scripts
	@uv tool run ruff check --fix $(SCRIPTS_DIR)/

# Website

.PHONY: configure
website-configure: ## setup website environment
	@cd $(WEBSITE_DIR); pnpm install

.PHONY: website-run
website-serve: _website-env ## run the website
	@cd $(WEBSITE_DIR); pnpm run dev

.PHONY: website-build
website-build: _website-env ## build the website
	@cd $(WEBSITE_DIR); pnpm run build

.PHONY: print-updates
website-print-updates: ## print list of outdated packages
	@cd $(WEBSITE_DIR); pnpm outdated

.PHONY: website-lint
website-lint: ## check preview website code quality
	@cd $(WEBSITE_DIR); pnpm lint

.PHONY: website-format
website-format: ## format preview website code
	@cd $(WEBSITE_DIR); pnpm format

.PHONY: _website-env
_website-env:
	uv run $(SCRIPTS_DIR)/website_env.py \
		generate \
		$(BUILD_DIR)/Lilex/ttf/Lilex-Regular.ttf \
		$(WEBSITE_DIR)/.env

# Install

.PHONY: install
install: ## install font to system (macOS and Linux only)
	@make install-$(OS)

.PHONY: install-Darwin
install-Darwin:
	@rm -rf ~/Library/Fonts/Lilex
	@cp -r $(BUILD_DIR)/Lilex/variable ~/Library/Fonts/Lilex

install-Linux:
	@rm -rf ~/.fonts/Lilex
	@cp -r $(BUILD_DIR)/Lilex/ttf ~/.fonts/Lilex

# Utilities

.PHONY: help
help: ## print this message
	@awk \
		'BEGIN {FS = ":.*?## "} \
		/^[a-zA-Z_-]+:.*?## / \
		{printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}' \
		$(MAKEFILE_LIST)

.PHONY: clean
clean: ## clean up artifacts
	@rm -rf $(BUILD_DIR)
	@rm -rf $(REPORTS_DIR)
	@rm -rf $(VENV_DIR)
