# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
This script sets up the path to SRILM programs.

The class 'Env' stores the path to SRILM
top-level directory, machine_type, and path to the programs.

In particular, the field of Env.programs is useful for accessing the path to the
SRILM programs.

An example of usage:

  import srienv
  env =  srienv.Env('/path/to/srilm')
  env.setup()

  # show the path to 'ngram-count'
  print env.programs['ngram-count']
"""

import os
import sys
import subprocess
import exceptions

programs = (
  'ngram',
  'ngram-count',
  'compute-best-mix',
)

class Error(exceptions.StandardError):
  pass

class MachineTypeError(Error):
  pass

class SRILMError(Error):
  pass

class FormatError(Error):
  pass

class Env(object):
  def __init__(self, home):
    self.home = home
    self.machine_type = None
    self.base_bin = None
    self.programs = {}

  def get_machine_type(self):
    '''SRILM's machine-type wrapper'''
    if self.home is None:
      print 'SRILM_HOME is None. you need to specify.specify'
      sys.exit(1)
    machine_type = os.path.join(self.home, 'sbin', 'machine-type')
    if not os.path.exists(machine_type):
      print 'machine-type is not found at {0}'.format(machine_type)
      raise

    cmd = [machine_type]
    try:
      process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    except:
      print '=========='
      print 'ERROR: {0}'.format(' '.join(sys.argv))
      print '=========='
      raise

    (stdout_content, err) = process.communicate()
    process.wait()
    self.machine_type = stdout_content.rstrip()
    return self.machine_type

  def _check_base_bin(self):
    if self.home is None:
      print 'ERROR: SRILM home is not specified.'
      raise
    if self.machine_type is None:
      self.get_machine_type()
    path = os.path.join(self.home, 'bin', self.machine_type)
    if os.path.exists(path):
      return path, True
    else:
      return path, False

  def setup(self):
    path, err = self._check_base_bin()
    if err == False:
      if self.machine_type == 'i686':
        # retry searching binaries by setting machine type is i686-m64.
        self.machine_type = 'i686-m64'
        self.setup()
      else:
        raise MachineTypeError('Unknown platform!')
    else:
      self.base_bin = path
      for p in programs:
        bin = os.path.join(self.base_bin, p)
        if not os.path.exists(bin):
          raise IOError('no such file or directory: {0}. '
                        'Have you compiled SRILM binaries?'.format(bin))
        if p not in self.programs:
          self.programs[p] = bin
