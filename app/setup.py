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

import setuptools


setuptools.setup(
    name = "snowflake-css",
    version = "1.3.1",
    url = "https://github.com/pietroalbini/snowflake-css",

    license = "GNU-GPL v3+",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.org",

    description = "My personal CSS components collection",
    long_description = __doc__,

    packages = [
        "snowflake_css",
    ],

    install_requires = [
        "pyscss",
        "rcssmin",
    ],

    extras_require = {
        "demo": [
            "jinja2",
            "django-htmlmin",
        ],
    },

    package_data = {
        "snowflake-css": [
            "*.scss",
            "*.html",
        ]
    },
    include_package_data = True,

    zip_safe = False,

    entry_points = {
        "console_scripts": [
            "snowflake-css = snowflake_css.__main__:main",
        ],
    },

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
