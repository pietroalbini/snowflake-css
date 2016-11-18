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

PYTHON = python3
EXECUTABLE = snowflake-css

BUILD_DIR = build
APP_DIR = app
COMPONENTS_DIR = components

# Get a list of the compoennts
COMPONENTS = $(patsubst $(COMPONENTS_DIR)/%,%,$(wildcard $(COMPONENTS_DIR)/*))


.PHONY: build demo
build: $(BUILD_DIR)/css/snowflake.css
demo: $(BUILD_DIR)/demo.html


$(BUILD_DIR)/env:
	@rm -rf $(BUILD_DIR)/env
	@mkdir -p $(BUILD_DIR)/env
	@$(PYTHON) -m virtualenv $(BUILD_DIR)/env
	@$(BUILD_DIR)/env/bin/pip install -e $(APP_DIR)[demo]


$(BUILD_DIR)/css/snowflake.css: $(BUILD_DIR)/env globals.scss $(patsubst %,$(COMPONENTS_DIR)/%/style.scss,$(COMPONENTS))
	@mkdir -p $(dir $@)
	@$(BUILD_DIR)/env/bin/$(EXECUTABLE) -o $@ --minify --


$(BUILD_DIR)/demo.html: $(BUILD_DIR)/env globals.scss $(patsubst %,$(COMPONENTS_DIR)/%/style.scss,$(COMPONENTS)) $(patsubst %,$(COMPONENTS_DIR)/%/demo.html,$(COMPONENTS)) $(APP_DIR)/snowflake_css/demo_template.html
	@mkdir -p $(dir $@)
	@$(BUILD_DIR)/env/bin/$(EXECUTABLE) --demo -o $@ --minify --


.PHONY: clean
clean:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(APP_DIR)/snowflake_css.egg-info
	@find -name "*.py[co]" -type f -delete
	@find -name __pycache__ -type d -delete
