# SPDX-License-Identifier: mit-only

# Copyright (C) 2022, Euan Mills.
# A simple Python script which recursively walks through the directory specified
# and returns the number of lines of code in the repository.

import os
import pathlib
import re
import sys

from sploinkd.utils.time import timed

ACCEPTED_FORMATS = [
    'py',
    'c',
    'h',
    'cpp',
    'cc',
    'hpp',
    'hp',
    's',
    'S',
    'sh',
    'ui',
    'bat',
    'ps1',
    'vim',
    'ini',
    'plist',
    'config',
    'conf',
    'pl',
    'php',
    'asm',
    'm4',
    'js',
    'jsx',
    'json',
    'ts',
    'tsx',
    'rb',
    'ex',
    'exs',
    'hs',
    'erl',
    'rebar',
    'java',
    'yaml',
    'toml',
    'xml',
    'html',
]

EXTENSION_REGEX = r"\.{}$"


def count_file(fp, verbose=False):
    try:
        if verbose:
            print(f"Counting: {fp}")
        with open(fp, "r")as f:
            lines = f.readlines()

        return len(lines)
    except Exception as e:
        if verbose:
            print(f"Exception reading from file {fp}: {e}")
    return -1


def walk_directories(dirname, ignore_node_modules=True, verbose=False):
    code_files = []
    for ext in ACCEPTED_FORMATS:
        if verbose:
            print(f"Searching for files with extension {ext.upper()}")
        for path, curr_dir, files in os.walk(dirname):
            for file in files:
                res = os.path.join(path, file)
                pattern = re.compile(EXTENSION_REGEX.format(ext))
                if (re.search(pattern, res)):
                    if ignore_node_modules:
                        if "node_modules" in res:
                            continue
                    if verbose:
                        print(f"Found {res}")
                    code_files.append(res)
    return code_files


def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('project', type=pathlib.Path,
                        help="The path to the project to scan.")
    parser.add_argument('-v', '--verbose', action="store_true",
                        help="Run loc in Verbose mode.")
    # Do we want to include node modules?
    parser.add_argument('-nM', '--node-modules', action="store_true",
                        help="Add this flag to include node_modules in search.")
    return parser.parse_args()

@timed
def main(args):
    project_dir = args.project
    if args.verbose:
        print(f"Project directory: {project_dir}.\n")

    if args.node_modules:
        print("Detection for node_modules/* is turned on. Did you mean this?")

    print("Scanning directories...")
    to_scan = walk_directories(project_dir,
                               ignore_node_modules=not args.node_modules,
                               verbose=args.verbose)

    print("Computing line count...")
    lines = 0
    errors = 0
    for source_file in to_scan:
        file_lines = count_file(source_file, verbose=args.verbose)
        if (file_lines < 0):
            errors += 1
            continue
        lines += file_lines

    error_rate = (errors / len(to_scan)) * 100
    
    if args.verbose:
        print("")

    print(f'\nProject \"{project_dir}\" has {lines} lines.')
    print(f'Processed {len(to_scan)} files with {errors} errors. '
          f'(error rate: {error_rate:.2f}%)')

    if error_rate > 1:
        print("\nA significant (>1%) number of errors were detected which may "
              "impact the accuracy of your results. Consider reporting a bug at "
              "https://github.com/Euab/pyloc")
    if error_rate > 70:
        print("\nWe detected that the vast majority of your files were "
              "unreadable. Consider checking if your files are corrupted or "
              "consider reporting a bug.")

if __name__ == "__main__":
    print("LOC Copyright (C) 2022, Euan Mills. All Rights Reserved.\n")
    try:
        sys.exit(main(get_args()))
    except KeyboardInterrupt:
        sys.exit(0)
