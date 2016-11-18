## Snowflake

Snowflake is my personal CSS components collection I use to avoid rewriting the
same style over and over again.

It's licensed under the MIT license.

### Available components

This repository contains multiple components you can use and a Python tool to
compile them. They're written in SCSS under the hood. The following components
are available:

 * `base`: basic styling for every page
 * `typography`: styling for documents and text

### Building

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
