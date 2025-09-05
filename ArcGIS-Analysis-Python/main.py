#!/usr/bin/env python3
# For relative imports to work in Python 3.6
#import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from src import version

##def main():
##    print(add('1', '1'))
##
##if __name__ == '__main__':
##    main()

from utils import some_function

def main():
    some_function()
    print(version.__version__)

if __name__ == "__main__":
    main()