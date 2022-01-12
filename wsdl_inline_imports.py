from loguru import logger
from pathlib import Path
from wsdl_inline_imports import process_file

import argparse
import sys
import os

def main():
    # set default log level at info
    if not os.getenv('LOGURU_LEVEL'):
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    parser = argparse.ArgumentParser(description='Inline external imports into a WSDL file.')
    parser.add_argument("-i", "--input", type=Path, help='input file', required=True)
    parser.add_argument("-o", "--output", type=Path, help='output file. If omitted print result to stdout')

    args = parser.parse_args()

    output = process_file(args.input)

    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
