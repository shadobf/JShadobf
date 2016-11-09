#!/usr/bin/env python
import sys
import traceback
import os


from jshadobf.common.convert import convert
from jshadobf.transformations.add_if_statement import add_if_statement


if __name__ == "__main__":
  #input = sys.stdin.read()
    if len (sys.argv) >1:
        prg = sys.argv[1]
    else:
        sys.exit()


    c = convert(prg)
    for _ in range(10):
        d = add_if_statement(c)
    print d
  
  
  