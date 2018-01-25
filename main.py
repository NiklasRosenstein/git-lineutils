
import argparse
import collections
import os
import sys
import git from './git'

parser = argparse.ArgumentParser(
  prog='git-lineutils',
  description='Find issues with line-endings in your repository.'
)
subparsers = parser.add_subparsers(dest='command')

detect_change_parser = subparsers.add_parser('detect-change')
detect_change_parser.add_argument('file', help='The file to detect a change in line-endings for.')
detect_change_parser.add_argument('--rev', default='HEAD', help='Start searching from the specified revision.')

show_parser = subparsers.add_parser('show')
show_parser.add_argument('file', help='The file to show the line-endings for.')
show_parser.add_argument('at', nargs='?', default='HEAD', help='The revision at which to read the file from.')
show_parser.add_argument('-b', '--branches', action='store_true', help='Show the line-endings in all branches.')
show_parser.add_argument('-a', '--all', action='store_true', help='Include remote branches.')
show_parser.add_argument('--unmerged', help='Exclude branches that are merged into the specified branch.')
show_parser.add_argument('--lf', action='store_true', help='Only show branches with LF.')
show_parser.add_argument('--crlf', action='store_true', help='Only show branches with CRLF.')

check_parser = subparsers.add_parser('check', description='Checks your Git configuration and makes suggestions.')


def get_line_endings(string):
  crlf_count = string.count(b'\r\n')
  lf_count = string.count(b'\n')
  if crlf_count != 0:
    if crlf_count != lf_count:
      raise ValueError('inconsistent CRLF ({}) and LF ({}) count.'
          .format(crlf_count, lf_count))
    return 'crlf'
  return 'lf'


def show(args):
  if args.branches:
    branches = git.branches(all=args.all)
    merged_branches = git.branches(merged_into=args.unmerged) if args.unmerged else []
    width = max(len(x) for x in branches)
    for branch in git.branches(all=args.all):
      if branch in merged_branches: continue
      try:
        line_endings = get_line_endings(git.get_file(branch, args.file))
      except git.DoesNotExist:
        continue
      if (not args.lf and not args.crlf) or (args.lf and line_endings == 'lf')\
          or (args.crlf and line_endings == 'crlf'):
        print('{} {}'.format(branch.ljust(width), line_endings.upper()))
  else:
    print(get_line_endings(git.get_file(args.at, args.file)).upper())


def detect_change(args):

  # Caches the line-endings for the file in a revision.
  le_cache = {}
  def get_le(rev):
    try:
      return le_cache[rev]
    except KeyError:
      pass
    try:
      result = get_line_endings(git.get_file(rev, args.file))
    except git.DoesNotExist as e:
      result = None
    le_cache[rev] = result
    return result

  try:
    args.rev = git.rev_parse(args.rev)
    commits = list(git.rev_list(args.rev))
    for index, rev in enumerate(commits):
      print('\r {}/{} ({})'.format(index, len(commits), rev), end='')
      revs = [rev] + git.parents(rev)
      le = [get_le(x) for x in revs]
      changed_indices = [i for i in range(1, len(le)) if le[i] and le[i] != le[0]]
      if changed_indices:
        print('\r', end='')
      for i in changed_indices:
        print('{}..{} ({}..{})'.format(revs[i], revs[0], le[i].upper(), le[0].upper()), end='')
        if len(revs) > 2:
          print(' merge-commit', end='')
        print()
  finally:
    print('\r')


def check(args):
  autocrlf = git.config('core.autocrlf') or 'false'
  if os.name == 'nt' and autocrlf != 'true':
    print('core.autocrlf: I recommend to set core.autocrlf=true on Windows (you have "{}")'.format(autocrlf))
  elif os.name != 'nt' and autocrlf != 'input':
    print('core.autocrlf: I recommend to set core.autocrlf=input on Unix platforms (you have "{}")'.format(autocrlf))
  else:
    print('core.autocrlf: Lookin\' good.')


def main(argv=None):
  args = parser.parse_args(argv)
  if not args.command:
    parser.print_usage()
    return 1
  return globals()[args.command.replace('-', '_')](args)


if require.main == module:
  sys.exit(main())
