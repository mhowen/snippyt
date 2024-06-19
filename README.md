# About
Snippyt CLI is a command-line application written in Python designed to parse
complex snippet objects from various standards and provide them to the system
clipboard in the absence of a language server.

Currently, VSCode Snippet syntax is recognized.

# System Requirements
Snippyt CLI is designed for use on UNIX- and POSIX-like systems. It interfaces
with the system clipboard by identifying the most suitable installed
clipboarding utility available in its execution environment. It is currently
compatible with the following utilities, which it checks for in list order:
- `xclip`
- `xsel`

Snippyt CLI requires at least one of the above to be locally installed in order
to provide Snippet data to the system clipboard.

Support for Wayland and `wl-copy` is planned and forthcoming.

# Usage
Snippyt CLI is best used in a terminal emulator in a window manager or
configured for invocation with userspace keybinds.

Command syntax:
```
snippyt SNIPPET [-h] [-p PREPROCESSOR] [-f [FILES...]]
```

## Sourcing Snippets
On startup, Snippyt CLI looks for `snippets.json` in its working directory. If
it is not present, it is created and populated with a handful of default
Snippets in VSCode Snippet syntax. You can manually add your own snippets to
this file, or read from one or more external files on your filesystem.

To read from external files, pass their paths to the `-f` option, e.g.:
```
snippyt <snippet name> -f ../Snippets/Python/base.json ../Snippets/Python/debug.json
```

## Preprocessing Snippets
You may wish to dynamically adjust the body of a snippet before providing it.
This can eliminate the need to source redundant copies of snippets whose bodies
are identical but for a few characters. To do so, pass the name of a supported
preprocessor to the `-p` option.

For example, to wrap a TeX snippet in block tokens:
```
snippyt <snippet name> -p tex-block
```
This will copy `$$<snippet body>$$` to the keyboard instead of the snippet body
alone.

Currently, the following preprocessor names are supported:
- `tex-inline`
- `tex-block`

