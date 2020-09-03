import argparse
import os
from typing import Optional, Sequence


def _process_line(line: bytes) -> bytes:
    if line.startswith(b'@db_helper()  #'):
        return b'@db_helper()\n'
    return line


def _fix_file(filename: str) -> bool:
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
    print(argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    args = parser.parse_args(argv)
    return_code = 0
    for filename in args.filenames:
        print(filename)
        _, extension = os.path.splitext(filename.lower())
        if _fix_file(filename):
            print(f'Fixing {filename}')  # noqa: T001
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
