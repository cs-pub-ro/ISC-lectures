# ISC slides makefile

S ?= $(firstword $(ALL_SLIDES))
LECTURE ?= $(S)

ALL_SLIDES = $(wildcard lectures/**/*.md)
OUT_DIR ?= dist
OUT_PDF ?= $(OUT_DIR)/lecture.pdf

PORT   ?= 3030
OPEN   ?= --open

.PHONY: install dev build export export-pptx export-png format clean

install: ## Install dependencies
	npm install

dev: ## Start dev server on PORT
	npx slidev --port $(PORT) $(OPEN) $(LECTURE)

build: ## Build static SPA into dist/
	npx slidev build $(LECTURE)

export: ## Export to PDF (OUT_PDF)
	npx slidev export --format pdf --output $(OUT_PDF) $(LECTURE)

export-pptx: ## Export to PPTX
	npx slidev export --format pptx --output $(OUT_PDF:.pdf=.pptx) $(LECTURE)

export-png: ## Export each slide to PNG
	npx slidev export --format png $(LECTURE)

format: ## Format slides markdown
	npx slidev format $(LECTURE)

clean: ## Remove build artifacts
	rm -rf dist node_modules/.vite $(OUT_PDF) $(OUT_PDF:.pdf=.pptx) slides.png

