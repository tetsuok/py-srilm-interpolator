#!/bin/sh
# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

os=`uname -s`

downloader="wget"

# OS X does not have wget by default...
if [ "$os" = "Darwin" ]; then
    downloader="curl -O"
fi

echo "Trying to download files from github"
header=https://github.com/downloads/tetsuok/py-srilm-interpolator

# Download only non-existent files.
for f in news-commentary-v6-lowercased-en-3gram.arpa.gz \
    news2008-en-3gram-arpa.gz \
    newstest2011-src-en-lowercased.txt.gz
do
    if ! [ -e $f ]; then
        $downloader $header/$f
    fi
done
