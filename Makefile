# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

all: check

DIR = srilm

check:
	python $(DIR)/setup.py test

clean:
	-rm -fr $(DIR)/*.pyc $(DIR)/tests/*.pyc
	-rm -fr *egg-info
