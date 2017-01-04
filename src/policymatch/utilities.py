#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Merge multiple text files by line-by-line."""

import argparse
import pathlib
import os


def get_lines(file_paths):
    """
    For all submitted file paths, yield the lines of each file as a set.

    :param file_paths: An iterable of pathlib.Path objects.
    :return:
    """
    for file_path in file_paths:
        with file_path.open(mode="r") as f:
            yield set(line.strip() for line in f)


def merge_lines(line_sets, merge_fun=set.union, sort=True):
    """
    Merge the contents of a list of sets of strings.

    :param line_sets: A list of sets of strings.
    :param merge_fun: A callable that merges sets
    :param sort: Sort the resulting merged entries.
    :return:
    """
    merged_lines = merge_fun(*line_sets)

    if sort:
        return tuple(sorted(merged_lines))
    else:
        return tuple(merged_lines)


def export_lines(lines, out_file=None):
    """
    Either export a list of strings to a file or print them to stdout.
    Can be used with pipes.

    :param lines: An iterable of strings
    :param out_file: None or a pathlib.Path object
    :return:
    """
    if out_file is not None:
        with out_file.open(mode="w") as f:
            for line in lines:
                f.write(line + os.linesep)
    else:
        for line in lines:
            print(line)


def main():
    """
    Merge text files line-by-line.
    """
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--union", help="perform a union", action="store_true")
    group.add_argument("-i", "--intersect", help="perform an intersection", action="store_true")
    group.add_argument("-d", "--difference", help="perform a difference", action="store_true")
    parser.add_argument("-s", "--sort", help="sort the merged entries", action="store_true")
    parser.add_argument("-o", "--out-file", help="write the resulting merge to a file", type=str)
    parser.add_argument("files", help="paths to the text files you wish to merge", type=str, nargs="+")
    args = parser.parse_args()

    # Create paths from the arguments
    file_paths = (pathlib.Path(p) for p in args.files)
    if args.out_file is not None:
        out_file = pathlib.Path(args.out_file)
    else:
        out_file = None

    # Load the masks into memory
    line_sets = get_lines(file_paths)

    # Generate the resulting merged masks
    if args.union:
        merge_fun = set.union
    elif args.intersect:
        merge_fun = set.intersection
    elif args.difference:
        merge_fun = set.symmetric_difference
    else:
        merge_fun = set.union

    merged_lines = merge_lines(line_sets, merge_fun, args.sort)

    # Write or print the merger
    export_lines(merged_lines, out_file)


if __name__ == "__main__":
    main()
