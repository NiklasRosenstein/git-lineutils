## git-lineutils

Find issues with line-endings in your repository.

> `usage: git-lineutils [-h] {detect-change,show} ...`

```
usage: git-lineutils detect-change [-h] [--rev REV] file

positional arguments:
  file        The file to detect a change in line-endings for.

optional arguments:
  -h, --help  show this help message and exit
  --rev REV   Start searching from the specified revision.
```

```
usage: git-lineutils show [-h] [-b] [-a] [--unmerged UNMERGED] [--lf] [--crlf]
                          file [at]

positional arguments:
  file                 The file to show the line-endings for.
  at                   The revision at which to read the file from.

optional arguments:
  -h, --help           show this help message and exit
  -b, --branches       Show the line-endings in all branches.
  -a, --all            Include remote branches.
  --unmerged UNMERGED  Exclude branches that are merged into the specified
                       branch.
  --lf                 Only show branches with LF.
  --crlf               Only show branches with CRLF.
```
