#!/usr/bin/env python3
import argparse
import os
import sys
from pocio import *

#########################
# Main exec
#########################
if __name__ == "__main__":
    print("" + sys.argv[0])

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action='store_true', help="set verbose")
    parser.add_argument("-l", "--showlines",
                        action='store_true', help="show occurency line number")
    parser.add_argument("-p", "--nocolor",
                        action='store_true', help="sPlain output, no color")
    parser.add_argument("searchpath", help="Path where search regex")
    parser.add_argument('-e', '--extension', nargs=1, required=True,
                        action='append', help='Set extension file where search [-e cpp -c h..]')
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode: " + str(args.verbose))

    if args.nocolor:
        print("No colored output set")

    cppfiles = MyFileFinder(args.searchpath, args.extension)
    for file in cppfiles.getAllFiles():
        cker = MyFileChecker()
        cker.set_file(file)

        cker.add_regex(MyRegex("short", "int16_t"))
        cker.add_regex(MyRegex("short int", "int16_t"))
        cker.add_regex(MyRegex("signed short", "int16_t"))
        cker.add_regex(MyRegex("signed short int", "int16_t"))
        cker.add_regex(MyRegex("unsigned short", "uint16_t"))
        cker.add_regex(MyRegex("unsigned short int", "uint16_t"))

        cker.add_regex(MyRegex("int", "int16_t"))
        cker.add_regex(MyRegex("signed", "int16_t"))
        cker.add_regex(MyRegex("signed int", "int16_t"))
        cker.add_regex(MyRegex("unsigned", "uint16_t"))
        cker.add_regex(MyRegex("unsigned int", "uint16_t"))

        cker.add_regex(MyRegex("long", "int32_t"))
        cker.add_regex(MyRegex("long int", "int32_t"))
        cker.add_regex(MyRegex("signed long", "int32_t"))
        cker.add_regex(MyRegex("signed long int", "int32_t"))
        cker.add_regex(MyRegex("unsigned long", "uint32_t"))
        cker.add_regex(MyRegex("unsigned long int", "uint32_t"))

        cker.add_regex(MyRegex("long long", "int64_t"))
        cker.add_regex(MyRegex("long long int", "int64_t"))
        cker.add_regex(MyRegex("signed long long", "int64_t"))
        cker.add_regex(MyRegex("signed long long int", "int64_t"))
        cker.add_regex(MyRegex("unsigned long long", "uint64_t"))
        cker.add_regex(MyRegex("unsigned long long int", "uint64_t"))

        cker.add_regex(MyRegex("uint", "uint16_t"))

        if os.isatty(sys.stdout.fileno()) and not args.nocolor:
            cker.print_with_color();

        cker.check()
        cker.print_res(args.verbose, args.showlines)
        del cker
