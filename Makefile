# Project paths
# BUNDLE_DIR = bundle
BUILD_DIR = build
REPORTS_DIR = reports
SCRIPTS_DIR = scripts
GLYPHS_FILE = sources/Lilex.glyphs

# Internal build variables
OS := $(shell uname)
VENV_DIR = ./venv
VENV = . $(VENV_DIR)/bin/activate;

define build-font
	@$(VENV) python $(SCRIPTS_DIR)/lilex.py build $(1)
endef

define check-font
	$(VENV) fontbakery check-$(2) \
		--auto-jobs \
		--full-lists \
		--html "$(REPORTS_DIR)/$(2)_$(1).html" \
		"$(BUILD_DIR)/$(1)/"*
endef

define check-ttf-file
	$(VENV) fontbakery check-$(2) \
		--auto-jobs \
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
configure: requirements.txt ## setup build environment
	@rm -rf $(VENV_DIR)
	@make $(VENV_DIR)
	@$(VENV) python -m youseedee A > /dev/null

.PHONY: configure
configure-preview: ## setup preview environment
	@cd preview; pnpm install

.PHONY: print-updates
print-updates: ## print list of outdated packages
	@$(VENV) pip list --outdated
	@cd preview; pnpm outdated

.PHONY: check
check: clean-reports ## check font quality
	@$(call check-font,"ttf","googlefonts")
	@$(call check-font,"variable","googlefonts")

.PHONY: check-sequential
check-sequential: clean-reports ## check each font file quality
	@$(call check-ttf-file,"Bold","googlefonts")
	@$(call check-ttf-file,"ExtraLight","googlefonts")
	@$(call check-ttf-file,"Medium","googlefonts")
	@$(call check-ttf-file,"Regular","googlefonts")
	@$(call check-ttf-file,"Thin","googlefonts")
	@$(call check-font,"variable","googlefonts")
		
.PHONY: lint
lint: ## check code quality
	$(VENV) ruff $(SCRIPTS_DIR)/
	$(VENV) pylint $(SCRIPTS_DIR)/
	cd preview; pnpm eslint 'src/**/*.{svlete,ts}'

.PHONY: preview
preview: ## show CLI special symbols preview
	@$(VENV) python $(SCRIPTS_DIR)/show.py

.PHONY: generate
generate: ## regenerate the font sources with classes and features
	@$(VENV) python $(SCRIPTS_DIR)/lilex.py generate

.PHONY: build
build: ## build the font
	@make clean-build
	@$(call build-font)

.PHONY: build-preview
build-preview: ## build the preview
	cd preview; pnpm run build

.PHONY: run-preview
run-preview: ## run the preview
	cd preview; pnpm run dev

# .PHONY: pack-bundle
# pack-bundle: ## pack the bundle
# 	rm -rf "$(BUNDLE_DIR)"
# 	mkdir "$(BUNDLE_DIR)"
# # Copy fonts
# 	cp -r "$(BUILD_DIR)/"* "$(BUNDLE_DIR)/"
# # Copy reports
# 	cp "$(REPORTS_DIR)/"* "$(BUNDLE_DIR)/"
# 	cd "$(BUNDLE_DIR)"; zip -r Lilex.zip ./*

# .PHONY: bundle
# bundle: ## build the bundle
# 	@make build
# 	@make check
# 	@make pack-bundle

.PHONY: release 
release:
	@make build

.PHONY: release-notes
release-notes:
	echo $(ARGS)
#	@mkdir -p ./$(BUILD_DIR)
#	$(VENV) python ./scripts/changelog.py notes Next > "./$(BUILD_DIR)/release-notes.md"

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

.PHONY: ttf
ttf: ## build ttf font
	$(call build-font,ttf)

.PHONY: otf
otf: ## build otf font
	$(call build-font,otf)

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

$(VENV_DIR): requirements.txt
	@rm -rf "$(VENV_DIR)"
	@python3.11 -m venv "$(VENV_DIR)"
	@$(VENV) pip install wheel
	@$(VENV) pip install -r requirements.txt
