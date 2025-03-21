.PHONY: confirm
_WARN := "\033[33m[%s]\033[0m %s\n"  # Yellow text for "printf"
_TITLE := "\033[32m[%s]\033[0m %s\n" # Green text for "printf"
_ERROR := "\033[31m[%s]\033[0m %s\n" # Red text for "printf"

CURRENT_BRANCH = $(shell git branch --show-current) 
COMMIT = $(shell git rev-parse --short=12 HEAD)

run-dev:
	poetry run python run.py

run-prod:
	poetry run gunicorn --config gunicorn_config.py run:app

save-db:
	fly ssh console -a nema-api -C "cat /data/wallet_db.db" > prod_sol_eth_wallets.db

deploy:
	@echo "Deploying to fly.io"
	fly deploy -c fly.toml

logs:
	@echo "Showing logs for nema-api"
	fly logs -a nema-api

# print-releases lists the last 5 releases for the nema-api deployment
print-releases:
	fly releases -a nema-api --image --json | jq 'limit(5; .[]) | {Version, Description, ImageRef, CreatedAt, UserEmail: .User.Email}'

# rollback rolls back the nema-api deployment to the specified IMAGE
rollback:
	@echo "Rolling back nema-api to ${IMAGE}"
	fly deploy -a nema-api --image ${IMAGE}

# ------------------------------------------------------------------------------
# Helpers

# Enforce the current branch is main
main-required:
	make branch-check CHECK_BRANCH="main"

# Check that the current branch is the provided CHECK_BRANCH
branch-check:
	@if [ "$$(git branch --show-current)" != "$(CHECK_BRANCH)" ]; then	\
		echo "$(tput setaf 3)WARNING: Current git branch is not $(CHECK_BRANCH): $$(git branch --show-current)"; \
		exit 1; \
	fi

# The CI environment variable can be set to a non-empty string,
# it'll bypass this command that will "return true", as a "yes" answer.
confirm:
	@if [[ -z "$(CI)" ]]; then \
		REPLY="" ; \
		read -p "⚠ Are you sure? [y/n] > " -r ; \
		if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
			printf $(_ERROR) "KO" "Stopping" ; \
			exit 1 ; \
		else \
			printf $(_TITLE) "OK" "Continuing" ; \
			exit 0; \
		fi \
	fi

	