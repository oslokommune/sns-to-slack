.DEV_PROFILE := okdata-dev
.PROD_PROFILE := okdata-prod

GLOBAL_PY := python3
# Named `.venv` so that SAM ignores it by default.
BUILD_VENV ?= .venv
BUILD_PY := $(BUILD_VENV)/bin/python

# Deployed Git revision, formatted as `<branch>:<short-sha>`.
GIT_REV = $(shell git rev-parse --abbrev-ref HEAD):$(shell git rev-parse --short=7 HEAD)

.PHONY: init
init: $(BUILD_VENV)

$(BUILD_VENV):
	$(GLOBAL_PY) -m venv $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip

.PHONY: format
format: $(BUILD_VENV)/bin/black
	$(BUILD_PY) -m black .

.PHONY: test
test: $(BUILD_VENV)/bin/tox
	$(BUILD_PY) -m tox -p auto -o

.PHONY: validate
validate:
	sam validate --lint --region eu-west-1

.PHONY: upgrade-deps
upgrade-deps: $(BUILD_VENV)/bin/pip-compile
	$(BUILD_VENV)/bin/pip-compile -U

.PHONY: deploy
deploy: login-dev init format test validate
	@echo "\nDeploying to stage: dev\n"
	sam build
	sam deploy --config-env dev --profile $(.DEV_PROFILE) --parameter-overrides "Stage=dev GitRev=$(GIT_REV)"

.PHONY: deploy-prod
deploy-prod: login-prod init format is-git-clean test validate
	sam build
	sam deploy --config-env prod --profile $(.PROD_PROFILE) --parameter-overrides "Stage=prod GitRev=$(GIT_REV)"

.PHONY: undeploy
undeploy: login-dev
	@echo "\nUndeploying stage: dev\n"
	sam delete --config-env dev --profile $(.DEV_PROFILE)

.PHONY: undeploy-prod
undeploy-prod: login-prod
	@echo "\nUndeploying stage: prod\n"
	sam delete --config-env prod --profile $(.PROD_PROFILE)

.PHONY: login-dev
login-dev:
	aws sts get-caller-identity --profile $(.DEV_PROFILE) || aws sso login --profile=$(.DEV_PROFILE)

.PHONY: login-prod
login-prod:
	aws sts get-caller-identity --profile $(.PROD_PROFILE) || aws sso login --profile=$(.PROD_PROFILE)

.PHONY: is-git-clean
is-git-clean:
	@status=$$(git fetch origin && git status -s -b) ;\
	if test "$${status}" != "## main...origin/main"; then \
		echo; \
		echo Git working directory is dirty, aborting >&2; \
		false; \
	fi

.PHONY: build
build: $(BUILD_VENV)/bin/wheel $(BUILD_VENV)/bin/twine
	$(BUILD_PY) setup.py sdist bdist_wheel

###
# Python build dependencies
##

$(BUILD_VENV)/bin/pip-compile: $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip-tools

$(BUILD_VENV)/bin/%: $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U $*
