# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import subprocess

def redirect(cmd, out_file):
  """Emulate redirection.
     $ cmd > out_file
  """
  try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               universal_newlines=True)
  except:
    print 'ERROR: %s' % ' '.join(cmd)
    raise

  (stdout_content, _) = process.communicate()
  with open(out_file, 'w') as fout:
    fout.write(stdout_content)
  return process.wait()

def run_or_die(cmd, msg):
  try:
    process = subprocess.Popen(cmd)
  except:
    print '=========='
    print 'ERROR: {0}'.format(msg)
    print '=========='
    raise
  process.wait()
