#!/usr/bin/python -tt
# Copyright 2015 Telenav Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
# http://stackoverflow.com/questions/11484700/python-example-for-reading-multiple-protobuf-messages-from-a-stream
import operator
import sys

def _VarintDecoder(mask):
    '''Like _VarintDecoder() but decodes signed values.'''

    local_ord = ord
    def DecodeVarint(buffer, pos):
        result = 0
        shift = 0
        while 1:
            b = local_ord(buffer[pos])
            result |= ((b & 0x7f) << shift)
            pos += 1
            if not (b & 0x80):
                if result > 0x7fffffffffffffff:
                    result -= (1 << 64)
                    result |= ~mask
                else:
                    result &= mask
                    return (result, pos)
            shift += 7
            if shift >= 64:
                ## need to create (and also catch) this exception class...
                raise _DecodeError('Too many bytes when decoding varint.')
    return DecodeVarint

## get a 64bit varint decoder
decoder = _VarintDecoder((1<<64) - 1)

## build map
def build_map(filename, here2ngx, ngx2here) :
  f = open(filename, 'rU')
  pos = 0
  data = f.read()
  datasize = len(data)
  while pos < datasize :
    newid, pos = decoder(data, pos)
    if (pos >= datasize) :
      break;
    origid, pos = decoder(data, pos)
    here2ngx[origid]  = newid
    ngx2here[newid]   = origid
  return True

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
  init = False;
  here2ngx = {}
  ngx2here = {}
  
  while True:
    print '1 = init filename'
    print '0 = exit'
    command = raw_input('<num>$ ')
    if command == '1':
      # show useage
      command = raw_input('<filename>$ ')
      filename = command
      build_map(filename, here2ngx, ngx2here)
      while True:
        print '1 = queryhereid'
        print '2 = queryngxid'
        print '3 = show all the mapping result in here2ngx'
        print '4 = show all the mapping result in ngx2here'
        print '0 = back'
        command = raw_input('<num>$ ')
        if command == '1':
          command = raw_input('<please input ngxid>$ ')
          print ngx2here.get(int(command))
        elif command == '2':
          command = raw_input('<please input hereid>$ ')
          print here2ngx.get(int(command))
        elif command == '3':
          for k,v in here2ngx.items() :
            print "here2ngx[%s] = " %k,v
        elif command == '4':
          for k,v in ngx2here.items() :
            print "ngx2here[%s] = " %k,v
        elif command == '0':
          break;
        else:
          print('invalid input')
    elif command == '0':
      sys.exit(1)
    else:
      print('invalid input')

if __name__ == '__main__':
  main()
