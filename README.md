py-srilm-interpolator
=====================

A python wrapper for determining interpolation weights with SRILM.
This package provides two features:

- Determine interpolation weights of multiple language models.
- Mix the models together in a single file.

Note that you should prepare for individual language models you want
to interpolate with SRILM before using this package.

Please note that *this script does NOT work without SRILM*.  You need
to install SRILM on your machine first.

I have tested scripts on Linux and OS X (10.8.2).

## Software Requirements ##

- [SRILM](http://www.speech.sri.com/projects/srilm/download.html)
- python [setuptools] (http://pypi.python.org/pypi/setuptools) (optional)

## Installation ##

The installation process is not necessary. Just download the pacakges on your favorite place.

    $ git clone git://github.com/tetsuok/py-srilm-interpolator.git

Usage
-----

There are three steps to create an interpolated language model.  To
run python scripts, you need to prepare for a config file first.

### Prepare for a config file ###

Here is a config file format you should prepare for first:

    [SRILM]
    # This is a comment. You need to edit the following line.
    home=/path/to/srilm

    # You need to edit the order of language model according to
    # the language models you want to mix together.
    opt=-order 3 -unk

    # Do not edit this option!
    [perplexity]
    opt=-debug 2

    [devset]
    # Edit the following path.
    path=/path/to/devset

    [language models]
    # Edit the following path.
    lm1=/path/to/lm1
    lm2=/path/to/lm2

WARNING: Basically you can change only values in the config file except the options in the
section "language models." In other words, do not change the name of 'sections' and
'options'; Python scripts will find the given sections and options.

Lines beginning with '#' or ';' are ignored and treated as comments.

Please see an example config file `example/example.cfg`.

In most cases, it will suffce to copy `example/example.cfg` and to
edit the path to SRILM, order of langauge models, and path to language
models.

I recomment using the absolute path to SRILM and language models when
you edit path to them.

### Determine interpolation weights ###

We assume that you have already prepared for a config file.

    $ ls
    config  py-srilm-interpolator
    $ py-srilm-interpolator/srilm/interpolator.py -c config [--cpus 2 ]

Please note that you need to specify `-c config`.

### Mix the models ###

    $ py-srilm-interpolator/srilm/combiner.py -c config best-mix.ppl

Please note that you need to specify `-c config`.
`best-mix.ppl` is a file which has been generated by the previous step.

References
----------

[Joshua Building large LMs with SRILM](http://joshua-decoder.org/4.0/large-lms.html)
