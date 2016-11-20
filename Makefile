# Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Executables
PYTHON = python3
GPG = gpg
TWINE = twine
EXECUTABLE = snowflake-css

# Configuration
NAME = snowflake-css
BUILD_DIR = build
APP_DIR = app
COMPONENTS_DIR = components
PACKAGES_DIR = $(BUILD_DIR)/packages

# Uploading configuration
RELEASES_SERVER = files@winter.net.pietroalbini.org
RELEASES_DIR = public/releases/$(NAME)/$(shell $(PYTHON) $(APP_DIR)/setup.py --version)

# Get a list of the compoennts
ALL_COMPONENTS = $(patsubst $(COMPONENTS_DIR)/%,%,$(wildcard $(COMPONENTS_DIR)/*))
COMPONENTS = $(filter-out base,$(ALL_COMPONENTS))


#########################
# CSS and demo building #
#########################

.PHONY: build demo

build: $(BUILD_DIR)/snowflake.css
demo: $(BUILD_DIR)/demo.html


$(BUILD_DIR)/env:
	@rm -rf $(BUILD_DIR)/env
	@mkdir -p $(BUILD_DIR)/env
	@$(PYTHON) -m virtualenv $(BUILD_DIR)/env
	@$(BUILD_DIR)/env/bin/pip install -e $(APP_DIR)[demo]


$(BUILD_DIR)/snowflake.css: $(BUILD_DIR)/env globals.scss $(patsubst %,$(COMPONENTS_DIR)/%/style.scss,$(ALL_COMPONENTS))
	@mkdir -p $(dir $@)
	@$(BUILD_DIR)/env/bin/$(EXECUTABLE) -o $@ --minify -- $(COMPONENTS)


$(BUILD_DIR)/demo.html: $(BUILD_DIR)/env globals.scss $(patsubst %,$(COMPONENTS_DIR)/%/style.scss,$(ALL_COMPONENTS)) $(patsubst %,$(COMPONENTS_DIR)/%/demo.html,$(ALL_COMPONENTS)) $(wildcard $(APP_DIR)/snowflake_css/demo/*)
	@mkdir -p $(dir $@)
	@$(BUILD_DIR)/env/bin/$(EXECUTABLE) --demo -o $@ --minify -- $(COMPONENTS)


########################################
# Python packages building and signing #
########################################

.PHONY: packages sign-packages upload

packages: $(PACKAGES_DIR)/*.tar.gz $(PACKAGES_DIR)/*.whl
sign-packages: $(addsuffix .asc,$(filter-out $(wildcard $(PACKAGES_DIR)/*.asc),$(wildcard $(PACKAGES_DIR)/*)))


PACKAGES_FILES = $(shell find -L app \( -name "*.py" -o -name "*.html" -o -name "*.scss" \) -type f -print)


$(PACKAGES_DIR)/*.tar.gz: $(PACKAGES_FILES)
	@mkdir -p $(PACKAGES_DIR)
	@cd $(APP_DIR) && $(PYTHON) setup.py sdist -d ../$(PACKAGES_DIR)
	@rm -rf $(APP_DIR)/build $(APP_DIR)/*.egg-info


$(PACKAGES_DIR)/*.whl: $(PACKAGES_FILES)
	@mkdir -p $(PACKAGES_DIR)
	@cd $(APP_DIR) && $(PYTHON) setup.py bdist_wheel -d ../$(PACKAGES_DIR)
	@rm -rf $(APP_DIR)/build $(APP_DIR)/*.egg-info


$(PACKAGES_DIR)/%.asc: $(PACKAGES_DIR)/%
	@$(GPG) --detach --armor --sign $(PACKAGES_DIR)/$*


upload: packages sign-packages
	@ssh $(RELEASES_SERVER) -- mkdir -p $(RELEASES_DIR)
	@scp $(PACKAGES_DIR)/* $(RELEASES_SERVER):$(RELEASES_DIR)
	@$(TWINE) upload --config-file .pypirc -r upload --skip-existing $(PACKAGES_OUT)/*


###########
# Cleanup #
###########

.PHONY: clean
clean:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(APP_DIR)/snowflake_css.egg-info
	@find -name "*.py[co]" -type f -delete
	@find -name __pycache__ -type d -delete
