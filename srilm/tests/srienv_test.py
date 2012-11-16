#!/usr/bin/env python
# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest
import srienv

class TestEnv(unittest.TestCase):

  def setUp(self):
    self.basepath = 'srilm/tests/dummy-srilm'
    self.env = srienv.Env(self.basepath)
    self.env.setup()

  def test_setup(self):
    self.assertEqual(self.env.machine_type, 'i686-m64')
    self.assertTrue(len(self.env.programs) > 0)
    self.assertTrue(self.env.programs['ngram'] is not None)
    self.assertTrue(self.env.programs['ngram-count'] is not None)
    self.assertTrue(self.env.programs['compute-best-mix'] is not None)
    self.assertEqual(self.env.programs.get('abracadabra'), None)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEnv)
  unittest.TextTestRunner(verbosity=2).run(suite)
