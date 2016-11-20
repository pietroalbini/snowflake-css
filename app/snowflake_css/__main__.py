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

DEMO_AVAILABLE = True

import sys

from . import compiler
try:
    from . import demo as demo_compiler
except ImportError:
    DEMO_AVAILABLE = False


def usage(exit_code):
    """Print the usage"""
    print(
        "Usage: snowflake-css [-h|--help] [-m|--min|--minify] "
        "[-o OUTPUT|--output OUTPUT] %s[-c COLOR|--color COLOR] "
        "[component [component ..]]" % ("[--demo] " if DEMO_AVAILABLE else "")
    )
    exit(exit_code)


def parse_args(args):
    """Parse the arguments"""
    color = None
    output = None
    demo = False
    minify = False
    components = []

    ask_color = False
    ask_output = False
    no_more_options = False

    for arg in args:
        if ask_color:
            color = arg
            ask_color = False
            continue

        if ask_output:
            output = arg
            ask_output = False
            continue

        if no_more_options or arg[0] != "-":
            components.append(arg)
            continue

        if arg == "--":
            no_more_options = True
            continue

        if arg in ("-h", "--help"):
            usage(0)

        if arg in ("-m", "--min", "--minify"):
            minify = True
            continue

        if arg in ("-c", "--color"):
            ask_color = True
            continue

        if arg in ("-o", "--output"):
            ask_output = True
            continue

        if arg == "--demo" and DEMO_AVAILABLE:
            demo = True
            continue

        usage(1)

    return components, {"minify": minify, "color": color}, output, demo


def main():
    """Main entry point of the tool"""
    args, kwargs, output, demo = parse_args(sys.argv[1:])

    if demo:
        del kwargs["minify"]
        result = demo_compiler.build(*args, **kwargs)
    else:
        result = compiler.build(*args, **kwargs)
    if output:
        with open(output, "w") as f:
            f.write(result)
            f.write("\n")
    else:
        print(result)


if __name__ == "__main__":
    main()
