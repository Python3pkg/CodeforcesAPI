#!/usr/bin/env python3

"""
In this example we are loading only unsolved Div2.C problems
"""

from collections import defaultdict
from itertools import groupby
import os
import sys

from codeforces import CodeforcesAPI
from codeforces import VerdictType
from codeforces import Problem
from codeforces import Contest
from six.moves import filter
import six


def first_or_default(lst, f):
    return next(filter(f, lst), None)


def get_contest_id(x):
    assert isinstance(x, (Problem, Contest))

    if isinstance(x, Problem):
        return x.contest_id
    else:
        return x.id


def group_by_contest_id(iterable):
    res = defaultdict(list)

    for k, vs in groupby(iterable, get_contest_id):
        res[k].extend(vs)

    return res


def make_url(problem):
    return 'http://codeforces.com/contest/{}/problem/{}'.format(problem.contest_id, problem.index)


def filter_div2(iterable):
    return filter(lambda contest: 'Div. 2' in contest.name, iterable)


def filter_c(iterable):
    return filter(lambda problem: 'C' in problem.index, iterable)


def filter_accepted(iterable):
    return filter(lambda submission: submission.verdict is not None and submission.verdict == VerdictType.ok, iterable)


def main(argv):
    assert len(argv) == 2

    api = CodeforcesAPI()

    print('Loading your submissions')
    handle = argv[1]
    submissions = filter_accepted(api.user_status(handle))
    solved_problems = filter_c(submission.problem for submission in submissions)
    solved_problems = set(solved_problems)
    six.print_(('Loaded {} solved C problems'.format(len(solved_problems))))

    print('Loading contests...')
    contests = group_by_contest_id(filter_div2(api.contest_list()))

    six.print_(('Loaded {} Div.2 contests'.format(len(contests))))

    print('Loading problemset...')
    problemset = api.problemset_problems()

    problems = group_by_contest_id(filter_c(problemset['problems']))

    stats = problemset['problemStatistics']
    stats = filter_c(stats)
    stats = filter(lambda s: s.contest_id in contests, stats)
    stats = filter(lambda s: problems[s.contest_id][0] not in solved_problems, stats)
    stats = sorted(stats, key=lambda s: s.solved_count, reverse=True)


    print()
    six.print_(('{:30}{:15}{}'.format('Name', 'Solved count', 'Url')))

    for stat in stats[:10]:
        problem = problems[stat.contest_id][0]
        six.print_(('{:30}{:<15}{}'.format(problem.name, stat.solved_count, make_url(problem))))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print('Invalid number of arguments')
        six.print_(('Usage: python3 {} [user handle]'.format(os.path.basename(sys.argv[0]))))
        sys.exit(1)
