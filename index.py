# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import click
import inspect
import sys

# Node.py and its dependencies that need to be inlined.
import nodepy
import six
import localimport

blobbify = require('./blobbify')

@click.command()
@click.option('--info', is_flag=True)
@click.option('-c', '--compress', is_flag=True)
@click.option('-m', '--minify', is_flag=True)
@click.option('-f', '--fullblob', is_flag=True)
@click.option('-o', '--output')
def main(info, compress, minify, fullblob, output):
  """
  Generate a standalone-version of the installed Node.py version by inlining
  its dependencies. Optionally, Node.py can be inlined as a Python-blob, too.
  """

  def blobbit(module, code=None):
    if code is None:
      code = inspect.getsource(sys.modules[module])
    return blobbify(module, code, compress=compress, minify=minify)

  source = inspect.getsource(nodepy)
  source = source.replace('import localimport', blobbit('localimport'), 1)
  source = source.replace('import six', blobbit('six'), 1)

  if fullblob:
    source = blobbit('nodepy', source)

  if not output:
    print(source)
  else:
    with open(output, 'w') as fp:
      fp.write(source)

if require.main == module:
  main()