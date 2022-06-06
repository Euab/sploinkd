# Create a C++ app

import os
import pathlib
import sys
from copy import deepcopy

from sploinkd.utils.time import timed
from sploinkd.utils.file import get_files

SYMBOL_USE_INCLUDE_START = b"// START-USE-INCLUDE"
SYMBOL_USE_INCLUDE_END   = b"// END-USE-INCLUDE"

TEMPLATE_PATH = os.path.dirname(os.path.abspath(__file__)) \
    + "/templates/create-cpp-app/"


def open_file(f):
    with open(f, 'rb') as f:
        data = f.readlines()
    
    return data


def write_file(f, data):
    with open(f, 'wb') as f:
        f.writelines(data)


def preprocess_template(using_include=False):
    print("📖 preprocessing template...")

    template_files = get_files(TEMPLATE_PATH)
    template_data = []
    to_write = []

    for template in template_files:
        if not using_include and 'include' in template:
            continue
        data = open_file(template)
        template_data.append((template, data))
    
    including = []
    removing = False
    for template in template_data:
        if not using_include:
            for line in template[1]:
                if SYMBOL_USE_INCLUDE_START in line:
                    removing = True
                    continue
                if SYMBOL_USE_INCLUDE_END in line:
                    removing = False
                    continue
                if removing:
                    continue

                including.append(line)
        
        else:
            for line in template[1]:
                if SYMBOL_USE_INCLUDE_START in line or SYMBOL_USE_INCLUDE_END \
                    in line:
                    continue
                including.append(line)

        to_write.append((template[0], deepcopy(including)))
        including.clear()
    
    return to_write


def write_template(to_write, to):
    location = os.path.abspath(
        to / to_write[0].split(TEMPLATE_PATH)[1]
    )
    dir = os.path.dirname(location)

    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    write_file(location, to_write[1])


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=pathlib.Path,
                        help="The path to sploink the project at.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Run in verbose")
    parser.add_argument("-i", "--include", action="store_true",
        help="Bootstrap project with an include directory.")

    args = parser.parse_args()
    return args


@timed
def main(args):
    fmt = "🌟 Creating a new C++ application at {} "
    if args.include:
        fmt += "with include template"
    fmt += '\n'
    
    print(fmt.format(args.project))

    to_write = preprocess_template(args.include)
    print("🪄 Sploinking template...")
    for template in to_write:
        write_template(template, args.project)

    print("\nCreated a new C++ project!\nWe suggest you start out by typing:"
        f"\n\ncd {args.project}\nmake\n./bin/myAwesomeApplication\n\n"
        "Happy hacking! 🤓")


if __name__ == '__main__':
    try:
        sys.exit(main(parse_args()))
    except KeyboardInterrupt:
        sys.exit(0)
