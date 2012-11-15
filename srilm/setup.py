# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages

setup(name = "py-srilm-interpolator",
      version = "0.0.1",
      packages = find_packages(),
      author = "Tetsuo Kiso",
      author_email = "tetsuo.sakai21@gmail.com",
      description = "A python wrapper for determining interpolation weights with SRILM.",
      license = "New BSD",
      keywords = "statistical machine translation, NLP, language modeling",
      url = 'https://github.com/tetsuok/py-srilm-interpolator',
      test_suite = "srilm.tests")
