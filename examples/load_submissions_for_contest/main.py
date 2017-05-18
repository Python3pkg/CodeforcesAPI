#!/usr/bin/env python3

"""
In this example we are loading submissions for contest by it's id
"""

import os
import sys

from codeforces import CodeforcesAPI
import six


def main(argv):
    api = CodeforcesAPI()

    contest_id = int(argv[1])

    submissions = api.contest_status(contest_id)

    six.print_(('{:^20}{}'.format('Submission ID', 'Party members')))

    for s in submissions:
        six.print_(('{:^20}{}'.format(s.id, ', '.join(member.handle for member in s.author.members))))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print("Invalid number of arguments")
        six.print_(("Usage: python {} [contest id]".format(os.path.basename(sys.argv[0]))))