# SPDX license identifier gpl2-only
#!/usr/bin/python3
#
# Copyright (C) 2022, Euan Mills.
# This file is a part of Sploinkd. See the file LICENSE for more information.
#
# File: le.py
#
# Abstract:
#     This script is able to convert between different line endings on a file
#     or project-wide basis.

import os
import pathlib
import sys
import time
from sploinkd.loc import walk_directories

EOL_CRLF = b'\r\n'
EOL_LF   = b'\n'


def read_file(file):
    with open(file, "rb") as f:
        data = f.read()

    return data


def write_file(file, data):
    with open(file, "wb") as f:
        f.write(data)


def convert_lf(file, verbose):
    try:
        if verbose:
            print(f"CRLF -> LF: {file}")

        data = read_file(file)
        data = data.replace(EOL_CRLF, EOL_LF)
        write_file(file, data)

    except Exception as e:
        if verbose:
            print(f"Error converting line endings in file: {file}. {e}")

        return False
    return True


def convert_crlf(file, verbose):
    try:
        convert_lf(file, verbose=False)

        if verbose:
            print(f"LF -> CRLF: {file}")

        data = read_file(file)
        data = data.replace(EOL_LF, EOL_CRLF)
        write_file(file, data)

    except Exception as e:
        if verbose:
            print(f"Error converting line endings in file: {file}. {e}")

        return False
    return True


def check_le(to_check, verbose):
    lf, crlf, mixed = 0, 0, 0
    errors = 0
    for codefile in to_check:
        try:
            data = read_file(codefile)
            
            if EOL_CRLF and EOL_LF in data:
                if verbose:
                    print(f"{codefile} - MIXED")
                mixed += 1

            if EOL_LF in data:
                if verbose:
                    print(f"{codefile} - LF")
                lf += 1

            if EOL_CRLF in data:
                if verbose:
                    print("f{file} - CRLF")
                crlf += 1

            else:
                print("{file} - Unknown")
                errors += 1
                continue

        except Exception as e:
            print(f"Exception checking file: {file}. {e}")
            errors += 1

    error_rate = (errors / len(to_check)) * 100
    pcnt_lf = (lf / len(to_check)) * 100
    pcnt_crlf = (crlf / len(to_check)) * 100
    pcnt_mixed = (mixed / len(to_check)) * 100

    fmt = ("Scan complete.\nFound {} files with {} errors.\nWith "
           "a line ending distribution of {}% LF : {}% CRLF : {}% mixed "
           "with {}% errors.")
    print(fmt.format(len(to_check), errors, pcnt_lf, pcnt_crlf, pcnt_mixed,
                     error_rate))
    sys.exit(0)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=pathlib.Path,
                        help="The path the the project where the requested "
                        "operation should be performed.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Run le in verbose")
    parser.add_argument("-lf", action="store_true", help="Convert to LF")
    parser.add_argument("-crlf", action="store_true", help="Convert to CRLF")
    parser.add_argument("-c", "--check", help="Check line endings only",
                        action="store_true")

    args = parser.parse_args()
    return args


def main(args):
    start = time.time()

    if not os.path.exists(args.project):
        print("Invalid project path supplied.")
        sys.exit(1)

    if args.check:
        check_le(args.project, args.verbose)

    if not args.lf and not args.crlf and not args.check:
        print("Please specify a conversion mode (LF/CRLF).")
        sys.exit(1)

    if args.lf and args.crlf:
        print("Please specify only one conversion mode.")

    if args.verbose:
        print(f"Project: {args.project}")

    print("Discovering files...")
    to_convert = walk_directories(args.project, verbose=args.verbose, ignore_node_modules=False)

    if args.check:
        check_le(to_convert, args.verbose)
    
    print(f"Converting {len(to_convert)} files...")

    count = 0
    errors = 0
    if args.lf:
        for project_file in to_convert:
            count += 1
            if not convert_lf(project_file, args.verbose):
                errors += 1
        return

    if args.verbose:
        print("Checking for preexisting CRLF...")
    for project_file in to_convert:
        count += 1
        if not convert_crlf(project_file, args.verbose):
            errors += 1

    now = time.time()
    error_rate = (errors / count) * 100
    print(f"\nProcessed {count} files with {errors} errors. "
          f"(error rate: {error_rate:.2f}%)")
    print(f"\nProcess completed. Time elapsed: {int(now - start)}s")


if __name__ == '__main__':
    print("SploinkD LineEnder Copyright (C) 2022, Euan Mills. All rights reserved.")
    try:
        sys.exit(main(parse_args()))
    except KeyboardInterrupt:
        sys.exit(0)

