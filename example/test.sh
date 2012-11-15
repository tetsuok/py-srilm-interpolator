#!/bin/sh
# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

for f in news-commentary-v6-lowercased-en-3gram.arpa.gz \
    news2008-en-3gram-arpa.gz \
    newstest2011-src-en-lowercased.txt.gz
do
    if ! [ -e $f ]; then
        echo "ERROR: ${f} does not exist!"
        echo "Download via download.sh"
        exit 1
    fi
done

../srilm/interpolator.py -c example.cfg --cpus 2

echo "Combine models..."
../srilm/combiner.py -c example.cfg best-mix.ppl
