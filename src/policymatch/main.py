#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Policymatch.py is an adaptation of PACK policygen.py that validates existing Hashcat masks against a password policy.
Based on PACK by The Sprawl at https://thesprawl.org/projects/pack/

Author: Eleanore Young
Copyright: 2017 scip AG
"""

import argparse
import pathlib

from .policy_matcher import PolicyMatcher
from .utilities import get_lines, merge_lines, export_lines


def main():
    parser = argparse.ArgumentParser(prog="policymatch", description="Validate hashcat masks against password policies.")
    parser.add_argument("files", type=str, nargs="+", help="paths to the files you wish to check and merge")
    parser.add_argument("-s", "--sort", help="sort the merged entries", action="store_true")
    parser.add_argument("-o", "--out-file", type=str, help="write the resulting data to a file")
    merge_group = parser.add_mutually_exclusive_group()
    merge_group.add_argument("-u", "--union", help="perform a union", action="store_true")
    merge_group.add_argument("-i", "--intersect", help="perform an intersection", action="store_true")
    merge_group.add_argument("-d", "--difference", help="perform a difference", action="store_true")
    policy_group = parser.add_argument_group()
    policy_group.add_argument("--min-lower", type=int, default=0, metavar="INT",
                              help="minimum number of lower case characters")
    policy_group.add_argument("--max-lower", type=int, default=-1, metavar="INT",
                              help="maximum number of lower case characters")
    policy_group.add_argument("--min-upper", type=int, default=0, metavar="INT",
                              help="minimum number of upper case characters")
    policy_group.add_argument("--max-upper", type=int, default=-1, metavar="INT",
                              help="maximum number of upper case characters")
    policy_group.add_argument("--min-digit", type=int, default=0, metavar="INT",
                              help="minimum number of digits")
    policy_group.add_argument("--max-digit", type=int, default=-1, metavar="INT",
                              help="maximum number of digits")
    policy_group.add_argument("--min-special", type=int, default=0, metavar="INT",
                              help="minimum number of special characters")
    policy_group.add_argument("--max-special", type=int, default=-1, metavar="INT",
                              help="maximum number of special characters")
    policy_group.add_argument("--min-length", type=int, default=8, metavar="INT",
                              help="minimum password length")
    policy_group.add_argument("--max-length", type=int, default=-1, metavar="INT",
                              help="maximum password length")
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

    # Check the merged masks for compliance
    matcher = PolicyMatcher(args.min_lower, args.max_lower, args.min_upper, args.max_upper,
                            args.min_digit, args.max_digit, args.min_special, args.max_special,
                            args.min_length, args.max_length)

    compliant_masks = matcher.get_compliant(merged_lines)

    # Write or print the merger
    export_lines(compliant_masks, out_file)


if __name__ == "__main__":
    main()
