.PHONY: setup sync bridge dev clean help

setup: ## Setup completo ambiente
	@echo "🚀 Setup Framework Antigravity + OpenCode"
	./scripts/install-opencode.sh
	./scripts/validate-agent-folder.sh
	python3 scripts/antigravity-opencode-bridge.py

sync: ## Sincronizza contesto tra ambienti
	python3 scripts/antigravity-opencode-bridge.py

bridge: ## Avvia bridge in background
	python3 scripts/antigravity-opencode-bridge.py &

dev: ## Modalità sviluppo (entrambi gli agenti)
	@echo "💻 Avvio ambiente di sviluppo integrato"
	@make bridge
	@antigravity . &
	@sleep 2
	@opencode attach

clean: ## Cleanup processi e cache
	@pkill -f "opencode serve" || true
	@pkill -f "antigravity-opencode-bridge" || true
	@echo "🧹 Cleanup completato"

help: ## Mostra questo help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
