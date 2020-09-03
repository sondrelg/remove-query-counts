from pre_commit_hooks.remove_query_counts import _process_line


def test_comment_without_kwarg():
    d = [
        (
            b'@db_helper(verbose=True)  # function ran 100000 times\r\n',
            b'@db_helper(verbose=True)\r\n'
        ),
        (
            b'          @db_helper(verbose=True)  # function ran a million times\r\n',
            b'          @db_helper(verbose=True)\r\n'
        ),
        (
            b'@db_helper(verbose=True)  # this comment was not generated automatically',
            b'@db_helper(verbose=True)  # this comment was not generated automatically'
        ),
    ]
    for _input, expected in d:
        result = _process_line(line=_input)
        assert result == expected
