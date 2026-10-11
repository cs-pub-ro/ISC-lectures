# ISC slides makefile

# S: alias for SLIDES_MD, default to first dir
S ?= $(firstword $(ALL_SLIDES))
SLIDES_MD ?= $(S)

ALL_SLIDES = $(wildcard lectures/**/slides.md)
OUT_DIR ?= dist
PROD ?=
EXPORT_PDFS ?=

NPX_ARGS = -q --no --loglevel=error --no-update-notifier
PORT   ?= 3030
OPEN   ?= --open


.PHONY: install dev build_all build clean

install: ## Install dependencies
	npm install

dev: ## Start dev server on PORT
	npx @slidev/cli --port $(PORT) $(OPEN) $(SLIDES_MS)

_OUT_ABS = $(abspath $(OUT_DIR))
build_all: ## Build all lectures + index into $(OUT_DIR)
	mkdir -p $(OUT_DIR)
	echo "<h1>ISC Lectures</h1><ul>" > "$(OUT_DIR)/index.html" && \
	for slides_md in $(ALL_SLIDES); do \
		LECTURE_NAME=$$(basename "$$(dirname "$$slides_md")") && \
		$(MAKE) build S="$$slides_md" ; \
		echo "<li><a href='$$LECTURE_NAME/'>$$LECTURE_NAME</a>" \
			"(<a href='$$LECTURE_NAME/slides.pdf'>PDF</a>)</li>" >> $(OUT_DIR)/index.html; \
	done; \
	echo "</ul>" >> "$(OUT_DIR)/index.html"

build: ## Builds & exports single lecture into $(OUT_DIR)
	LECTURE_NAME=$$(basename "$$(dirname "$(SLIDES_MD)")") && \
	export NODE_NO_WARNINGS=1 && \
	echo "Building HTML for $$LECTURE_NAME..." && \
	npx $(NPX_ARGS) @slidev/cli build "$(SLIDES_MD)" \
		--base "$(if $(PROD),/ISC-lectures)/$$LECTURE_NAME/" \
		--out "$(_OUT_ABS)/$$LECTURE_NAME" && \
	if [[ "$(EXPORT_PDFS)" == "1" ]]; then \
		echo "Building PDF for $$LECTURE_NAME..." && \
		npx $(NPX_ARGS) @slidev/cli export "$(SLIDES_MD)" --format pdf \
			--output "$(_OUT_ABS)/$$LECTURE_NAME/slides.pdf"; \
	fi
	

clean: ## Remove build artifacts
	rm -rf $(OUT_DIR) node_modules/.vite

