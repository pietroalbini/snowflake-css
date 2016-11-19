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

import jinja2
from htmlmin.minify import html_minify
import rcssmin

from . import compiler


def render_template(path, ctx):
    """Render a Jinja2 template"""
    with path.open() as f:
        content = f.read()

    tmpl = jinja2.Template(content)
    return html_minify(tmpl.render(**ctx))


def build(*components, color=None):
    """Build the demo page"""
    components = list(components)
    base = pathlib.Path(__file__).parent

    # Get the demo CSS
    with (base / "demo" / "style.css").open() as f:
        css_demo = rcssmin.cssmin(f.read())

    # Get the source CSS
    css = compiler.build(*components, color=color, minify=True)

    # Always build the base component
    components.insert(0, "base")

    # Load the source of all the components' demos
    demos = []
    for component in components:
        path = base / "components" / component / "demo.html"
        with path.open() as f:
            demos.append({"name": component, "src": f.read()})

    return render_template(base / "demo" / "template.html", {
        "css": css,
        "css_demo": css_demo,
        "demos": demos,
    })
