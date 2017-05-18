#!/usr/bin/env python3

"""
In this example we are loading users by their handles
"""

from codeforces import CodeforcesAPI
import six


def main():
    api = CodeforcesAPI()

    handles = ['soon', 'DmitriyH', 'Fefer_Ivan']

    users = api.user_info(handles)

    for u in users:
        six.print_(('{}, rank: {}'.format(u.handle, u.rank)))


if __name__ == '__main__':
    main()
