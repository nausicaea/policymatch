Policymatch
===========
Policymatch.py is an adaptation of PACK policygen.py that validates existing
Hashcat masks against a password policy.

Based on PACK by The Sprawl at https://thesprawl.org/projects/pack/

Usage
-----
.. code::

    usage: policymatch [-h] [-s] [-o OUT_FILE] [-u | -i | -d] [--min-lower INT]
                   [--max-lower INT] [--min-upper INT] [--max-upper INT]
                   [--min-digit INT] [--max-digit INT] [--min-special INT]
                   [--max-special INT] [--min-length INT] [--max-length INT]
                   files [files ...]

    Validate hashcat masks against password policies.

    positional arguments:
      files                 paths to the files you wish to check and merge

    optional arguments:
      -h, --help            show this help message and exit
      -s, --sort            sort the merged entries
      -o OUT_FILE, --out-file OUT_FILE
                            write the resulting data to a file
      -u, --union           perform a union
      -i, --intersect       perform an intersection
      -d, --difference      perform a difference

      --min-lower INT       minimum number of lower case characters
      --max-lower INT       maximum number of lower case characters (-1 for
                            unbounded)
      --min-upper INT       minimum number of upper case characters
      --max-upper INT       maximum number of upper case characters (-1 for
                            unbounded)
      --min-digit INT       minimum number of digits
      --max-digit INT       maximum number of digits (-1 for unbounded)
      --min-special INT     minimum number of special characters
      --max-special INT     maximum number of special characters (-1 for
                            unbounded)
      --min-length INT      minimum password length
      --max-length INT      maximum password length (-1 for unbounded)