import argparse
import os
import re
from typing import Optional, Sequence

_comment_pattern = re.compile(b'\s*@db_helper\(([\w]{0,15}=[\w]{0,15}|[\w]{0,15})\)  # function ran ')


def _process_line(line: bytes) -> bytes:
    """
    Replaces the @db_helper-appended comment with a cleaned version of itself.
    """
    if _comment_pattern.match(line):
        starting_index = line.find(b'@db_helper(')
        possible_whitespace = line[:starting_index]
        possible_args_or_kwargs = line[line.find(b'(') + 1: line.find(b')')]
        return possible_whitespace + b'@db_helper(' + possible_args_or_kwargs + b')\r\n'
    return line


def _fix_file(filename: str) -> bool:
    """
    Iterates through a files lines and cleans any comments.
    """
    with open(filename, mode='rb') as file_processed:
        lines = file_processed.readlines()
    newlines = [_process_line(line) for line in lines]
    if newlines != lines:
        with open(filename, mode='wb') as file_processed:
            for line in newlines:
                file_processed.write(line)
        return True
    else:
        return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    args = parser.parse_args(argv)
    return_code = 0
    for filename in args.filenames:
        _, extension = os.path.splitext(filename.lower())
        if _fix_file(filename):
            print(f'Fixing {filename}')  # noqa: T001
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
