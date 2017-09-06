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

import pathlib

from scss.compiler import compile_string as scss_compile
import rcssmin


DEFAULT_COLOR = "#2266bb"


def minify(input):
    """Minify a bunch of CSS"""
    return rcssmin.cssmin(input)


def compile(*sources, color=None):
    """Compile multiple SCSS sources together"""
    if color is None:
        color = DEFAULT_COLOR

    parts = []
    parts.append("$color_main: %s;" % color)

    # Include all the sources
    for source in sources:
        # Read the content of the source file
        with source.open() as f:
            content = f.read()

        parts.append(content)

    return scss_compile("\n".join(parts))


def build(*components, color=None, minify=False):
    """Build multiple components"""
    base = pathlib.Path(__file__).parent
    to_build = [
        base / "globals.scss",
        base / "components" / "base" / "style.scss",
    ]

    # Check if components are valid
    for component in components:
        path = base / "components" / component / "style.scss"

        if not path.exists():
            raise NameError("Component %s doesn't exist" % component)

        to_build.append(path)

    # Build the CSS files
    result = compile(*to_build, color=color)
    if minify:
        result = rcssmin.cssmin(result)

    return result
