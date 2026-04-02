.PHONY: setup run demo clean

# Setup - install all dependencies with uv
setup:
	uv sync
	@echo "Setup complete. Run 'make run' or 'uv run jupyter lab' to start."

# Run Jupyter Lab
run:
	uv run jupyter lab

# Run the demo agent locally
demo:
	cd demo && cp ../.env .env 2>/dev/null || true && uv run langgraph dev

# Clean up
clean:
	rm -rf .venv uv.lock
