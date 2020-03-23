#!/usr/bin/env python3
import argparse
from pocio import *

#########################
# Main exec
#########################
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action='store_true', help="set verbose")
    parser.add_argument("-l", "--showlines",
                        action='store_true', help="show occurency line number")
    parser.add_argument("searchpath", help="Path where search regex")
    parser.add_argument('-e', '--extension', nargs=1, required=True,
                        action='append', help='Set extension file where search [-e cpp -c h..]')
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode: " + str(args.verbose))

    cppfiles = MyFileFinder(args.searchpath, args.extension)

    for file in cppfiles.getAllFiles():
        cker = MyFileChecker()
        cker.set_file(file)

        cker.add_regex(MyRegex(
            "short[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "short", "int16_t"))
        cker.add_regex(MyRegex(
            "short int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "short int", "int16_t"))
        cker.add_regex(MyRegex(
            "signed short[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed short", "int16_t"))
        cker.add_regex(MyRegex(
            "signed short int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed short int", "int16_t"))
        cker.add_regex(MyRegex(
            "unsigned short[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned short", "uint16_t"))
        cker.add_regex(MyRegex(
            "unsigned short int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned short int", "uint16_t"))

        cker.add_regex(MyRegex(
            "int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "int", "int16_t"))
        cker.add_regex(MyRegex(
            "signed[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed", "int16_t"))
        cker.add_regex(MyRegex(
            "signed int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed int", "int16_t"))
        cker.add_regex(MyRegex(
            "unsigned[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned", "uint16_t"))
        cker.add_regex(MyRegex(
            "unsigned int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned int", "uint16_t"))

        cker.add_regex(MyRegex(
            "long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "long", "int32_t"))
        cker.add_regex(MyRegex(
            "long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "long int", "int32_t"))
        cker.add_regex(MyRegex(
            "signed long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed long", "int32_t"))
        cker.add_regex(MyRegex(
            "signed long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed long int", "int32_t"))
        cker.add_regex(MyRegex(
            "unsigned long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned long", "uint32_t"))
        cker.add_regex(MyRegex(
            "unsigned long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned long int", "uint32_t"))

        cker.add_regex(MyRegex(
            "long long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "long long", "int64_t"))
        cker.add_regex(MyRegex(
            "long long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "long long int", "int64_t"))
        cker.add_regex(MyRegex(
            "signed long long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed long long", "int64_t"))
        cker.add_regex(MyRegex(
            "signed long long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "signed long long int", "int64_t"))
        cker.add_regex(MyRegex(
            "unsigned long long[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned long long", "uint64_t"))
        cker.add_regex(MyRegex(
            "unsigned long long int[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "unsigned long long int", "uint64_t"))

        cker.add_regex(MyRegex(
            "uint[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}",
            "uint", "uint16_t"))




        cker.check()
        cker.print_res(args.verbose, args.showlines)
        del cker
