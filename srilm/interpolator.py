#!/usr/bin/env python
# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
Determine interpolation weights of specified language models in a config file.

Sample usage:
  $ python interpolator.py -c config --cpus 4

'config' is a config file; see example/example.cfg
"""

import multiprocessing
import optparse
import os
import shlex
import subprocess
import sys
import tempfile
from ConfigParser import ConfigParser

import srienv

parser = optparse.OptionParser(usage='%prog [options]')
parser.add_option('-c', '--config', dest='conf',
                  default=None, help='Path to config files (mandatory).')
parser.add_option('-o', '--out', dest='out',
                  default='best-mix.ppl', help='Path to the file that contains the best lambdas')
parser.add_option('--cpus', dest='cpus', type='int',
                  default=1, help='Number of processes to be used when computing perplexities.')

logs = sys.stderr

def rearrange_cpus(config, opts):
  lms = config.items('language models')
  if len(lms) < opts.cpus:
    opts.cpus = len(lms)

def _calc_perplexity(cmd_str):
  print >>logs, multiprocessing.current_process().name, 'executing: {0}'.format(cmd_str)
  cmds = shlex.split(cmd_str)
  cmd = cmds[:-1]
  out_file = cmds[-1]

  try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               universal_newlines=True)
  except:
    print 'ERROR: %s' % cmd_str
    raise

  (stdout_content, _) = process.communicate()
  with open(out_file, 'w') as fout:
    fout.write(stdout_content)
  return process.wait()

def setup_perplexity_tasks(env, opts, lms, devset, tmpdir):
  cmd = env.programs['ngram']
  tasks = ['{0} {1} -lm {2} -ppl {3} {4}'.format(
      cmd, opts, lm[1], devset, os.path.join(tmpdir, lm[0] + '.ppl')) for lm in lms]
  return tasks

def calc_perplexity(env, config, tmpdir, cpus):
  devset = config.get('devset', 'path')
  if not os.path.exists(devset):
    raise IOError('devset is not found %s' % devset)

  lms = config.items('language models')
  perplexity_opts = config.get('perplexity', 'opt') + ' ' + config.get('SRILM', 'opt')
  tasks = setup_perplexity_tasks(env, perplexity_opts, lms, devset, tmpdir)

  print >>logs, 'Computing perplexities for each language model on the devset: {0}'.format(devset)
  pool = multiprocessing.Pool(cpus)
  pool.map(_calc_perplexity, tasks)
  print >>logs, 'Resulting perplexity files are written to {0}'.format(tmpdir)

def compute_best_mix(bin, lms, tmpdir, out):
  files = [os.path.join(tmpdir, lm[0] + '.ppl') for lm in lms]
  cmd = [bin] + files
  print >>logs, 'Executing {0} > {1}'.format(' '.join(cmd), out)
  try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               universal_newlines=True)
  except:
    print 'ERROR: {0}'.format(' '.join(cmd))
    raise
  (stdout_content, _) = process.communicate()

  with open(out, 'w') as fout:
    fout.write(stdout_content)
  return process.wait()

def main_internal(argv):
  opts, unused_args = parser.parse_args(argv[1:])
  if opts.conf is None:
    print >>logs, 'Config file is not specified.'
    parser.print_help()
    sys.exit(1)

  config = ConfigParser()
  config.read(opts.conf)
  env = srienv.Env(config.get('SRILM', 'home'))
  env.setup()
  rearrange_cpus(config, opts)

  tmpdir = tempfile.mkdtemp()

  calc_perplexity(env, config, tmpdir, opts.cpus)

  print >>logs, 'Now estimating the best interpolation weights...'
  compute_best_mix(env.programs['compute-best-mix'],
                   config.items('language models'), tmpdir, opts.out)
  print >>logs, 'Saving the best interpolation weights to {0}'.format(opts.out)

def main():
  try:
    main_internal(sys.argv)
  except KeyboardInterrupt:
    print 'Interrupted'
    sys.exit(1)

if __name__ == '__main__':
  main()
