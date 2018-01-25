
import re
import subprocess


class DoesNotExist(ValueError):
  pass


def parents(rev):
  " Returns a list of the parent commit IDs. "
  args = ['git', 'cat-file', '-p', rev]
  output = subprocess.check_output(args, stderr=subprocess.PIPE)
  return re.findall('parent\s+([\w\d]+)', output.decode())


def get_file(rev, file):
  " Returns the a file at the specified revision as binary string. "
  args = ['git', 'show', '{}:{}'.format(rev, file)]
  try:
    return subprocess.check_output(args, stderr=subprocess.PIPE)
  except subprocess.CalledProcessError as e:
    if e.returncode == 128:
      raise DoesNotExist(e.stderr.decode().strip())
    raise


def short(rev):
  " Returns the short form of a revisions commit ID. "
  args = ['git', 'rev-parse', rev]
  output = subprocess.check_output(args, stderr=subprocess.PIPE)
  return output.decode().strip()[:10]


def branches(all=False, merged_into=None):
  " Returns a list of branches in the repository. "
  if merged_into:
    args = ['git', 'branch', '--merged', merged_into]
    output = subprocess.check_output(args, stderr=subprocess.PIPE).decode()
    return output.split()
  else:
    args = ['git', 'branch']
    if all:
      args += ['-a']
    result = []
    output = subprocess.check_output(args, stderr=subprocess.PIPE).decode()
    for line in output.split('\n'):
      parts = line.split()
      if not parts: continue
      if parts[0] == '*': parts.pop(0)
      result.append(parts[0].strip())
    return result
