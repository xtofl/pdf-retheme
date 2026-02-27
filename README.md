# Retheme PDFs

PDFs and other documents are often too decorated to be consumed.

This package allows you to retheme them, e.g. to black-and-white,
so you don't need all of your ink when printing it.

## Installing

We recommend using [pipx] to install this package in its own virtual
environment.


[pipx]: https://pipx.pypa.io/stable/installation/

```shell
$ pipx install retheme-pdf
...
```


## Usage

```shell
$ retheme-pdf path/to/my.colorful.pdf path/to/my.black-and-white.pdf
Processing page 1/92...
Processing page 2/92...
Processing page 3/92...
Processing page 4/92...
...
```
