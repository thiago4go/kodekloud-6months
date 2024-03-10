# Vi Tricks

## Find and Replace

If no `[range]` and `[count]` are given, only the pattern found in the current line is replaced. The current line is the line where the cursor is placed.

For example, to search for the first occurrence of the string ‘foo’ in the current line and replace it with ‘bar’, you would use:

```vi
:s/foo/bar/
```

To replace all occurrences of the search pattern in the current line, add the `g` flag:

```vi
:s/foo/bar/g
```

If you want to search and replace the pattern in the entire file, use the percentage character `%` as a range. This character indicates a range from the first to the last line of the file:

```vi
:%s/foo/bar/g
```

If the `{string}` part is omitted, it is considered as an empty string, and the matched pattern is deleted. The following command deletes all instances of the string ‘foo’ in the current line:

```vi
:s/foo//g
```

Instead of the slash character (`/`), you can use any other non-alphanumeric single-byte character except as a delimiter. This option is useful when you have the ‘/’ character in the search pattern or the replacement string.

```vi
:s|foo|bar|
```

\
