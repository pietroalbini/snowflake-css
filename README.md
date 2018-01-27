# Snowflake

Snowflake is my personal CSS components collection I use to avoid rewriting the
same style over and over again.

It's licensed under the MIT license.

## Available components

This repository contains multiple components you can use and a Python tool to
compile them. They're written in SCSS under the hood. The following components
are available:

* `base`: basic styling for every page
* `button`: styling for buttons
* `footer`: styling for footers
* `inline-list`: styling for inline lists
* `navbar`: a simple responsive navbar
* `pygments-theme`: theme for Pygments code highlights
* `sidebar`: a simple sidebar, toggleable on mobile
* `typography`: styling for documents and text

## Building

The easiest way to build Snowflake is to invoke `make`, which will build
everything for you. Be sure to have Python 3 and virtualenv installed:

```
$ make
```

The resulting CSS file will be in `build/css/snowflake.css`. If you want to see
a demo page instead just build the `demo` target:

```
$ make demo
```

## Integrating with your website

Even if you can directly put the Snowflake css file in your website, it's not
the best solution available. Snowflake is made to be modular, and it's better
to include only the components you need. There is the `snowflake-css`
command-line utility which allows you to build only what you want.

You can install it from PyPI with `pip`:

```
$ python3 -m pip install snowflake-css
```

Then, you can call it with the components you want as argument (keep in mind
the `base` component is always included):

```
$ snowflake-css typography inline-list
```

You can also pass the `-m` flag to minify the output, or `-o output.css` to
save the result in the `output.css` file, instead of printing it to the
standard output.
