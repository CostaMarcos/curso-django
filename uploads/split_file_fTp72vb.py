#!/usr/bin/env python

import sys
import os
import math
import re
from subprocess import call
import hashlib

MIN_PART_SIZE = 1024 * 1024
DEFAULT_PART_SIZE = 16 * 1024 * 1024
DEFAULT_PART_BASE = '.part'

def usage(argv):
    print >> sys.stdout, ''
    print >> sys.stdout, 'Usage: %s <file> [<size>]' % argv[0]
    print >> sys.stdout, ''
    print >> sys.stdout, '  Minimum part size is %d' % (MIN_PART_SIZE,)
    print >> sys.stdout, '  Default part size is %d' % (DEFAULT_PART_SIZE,)
    print >> sys.stdout, ''

if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print >> sys.stderr, 'ERROR: invalid number of arguments'
    usage(sys.argv)
    sys.exit(1)

file_name = sys.argv[1]

if (len(sys.argv) == 3):
    part_size = int(sys.argv[2])
else:
    part_size = DEFAULT_PART_SIZE

if (part_size <= 0 or part_size < MIN_PART_SIZE):
    print >> sys.stderr, 'ERROR: invalid part size'
    sys.exit(1)

if not os.path.isfile(file_name):
    print >> sys.stderr, 'ERROR: file does not exist'
    sys.exit(1)

file_size = os.path.getsize(file_name)
parts = int(math.ceil(float(file_size)/float(part_size)))
digits = int((math.log10(parts) + 1))

if file_size <= part_size:
    print >> sys.stderr, 'ERROR: file size is smaller than or equal to the part size'
    sys.exit(1)

# TODO: make the part base configurable
part_base = DEFAULT_PART_BASE

match = re.match('^(([A-Z0-9_]+)-ota-([A-Z]+[0-9]{10})-(from-([A-Z]+[0-9]{10})|full))(\.[^.]+)$', file_name)
if not match:
    print >> sys.stderr, 'ERROR: could not parse filename'
    print >> sys.stderr, 'Filename must be "PRODUCT-ota-NEWVERSION-from-OLDVERSION.zip" or'
    print >> sys.stderr, '                 "PRODUCT-ota-NEWVERSION-full.zip".'
    print >> sys.stderr, ''
    print >> sys.stderr, 'NEWVERSION and OLDVERSION must be LLLL[...]YYYYMMDDNN'
    print >> sys.stderr, ''
    sys.exit(1)

file_prefix = match.group(1)
product = match.group(2)
newversion = match.group(3)
oldversion = match.group(5)
file_sufix = match.group(6)

print >> sys.stdout, 'File name: %s (prefix=%s  sufix=%s)' % (file_name, file_prefix, file_sufix)
print >> sys.stdout, 'File size: %d' % (file_size,)
print >> sys.stdout, 'Part size: %d' % (part_size,)
print >> sys.stdout, 'Parts: %d' % (parts,)
print >> sys.stdout, 'Digits: %d' % (digits,)

call([ '/usr/bin/split',
       '--verbose',
       '--suffix-length=%s' % (digits,),
       '--bytes=%d' % (part_size,),
       '--additional-suffix=%s' % (file_sufix,),
       '--numeric-suffixes',
       file_name, '%s%s' % (file_prefix, part_base) ])

def sha1OfFile(filepath, join_sha):
    sha = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # one-megabyte block
            if not block: break
            sha.update(block)
            if join_sha: join_sha.update(block)
        return sha.hexdigest()

print >> sys.stdout, ''
print >> sys.stdout, 'DB Template:'
print >> sys.stdout, ''
print >> sys.stdout, '''info = SplittedUpdateInfo('%s/%s', '%s')''' % (product, newversion, file_prefix)

join_sha = hashlib.sha1()
for i in range(0, parts):
    part_file_name = '''%s%s%s%s''' % (file_prefix, part_base, str(i).zfill(digits), file_sufix)
    part_file_size = os.path.getsize(part_file_name)
    part_file_hash = sha1OfFile(part_file_name, join_sha)
    print >> sys.stdout, '''info.add_part(%i, '%s')''' % (part_file_size, part_file_hash)
print >> sys.stdout, '''info.commit()'''
print >> sys.stdout, ''

print >> sys.stdout, '''Verifying checksum of joined files...'''
original_hash = sha1OfFile(file_name, None)
joined_hash = join_sha.hexdigest()
if original_hash != joined_hash:
    print >> sys.stdout, ''
    print >> sys.stdout, '''******* ERROR!!! HASH MISMATCH!!! *******'''
    print >> sys.stdout, ''
else:
    print >> sys.stdout, '''OK'''
