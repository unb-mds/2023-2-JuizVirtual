# Contributing Rules

- The development will be done **in English**.
- Commit messages **must** follow
[Conventional Commits specifications](https://www.conventionalcommits.org/en/v1.0.0/#specification).
- Branches **must** follow the
[Git Flow pattern](https://github.com/nvie/gitflow).
- Versioning must follow the
[Semantic Versioning specifications](https://semver.org/).
- Every contribution **must** be accompanied by a test suite that tests the new
feature or simulates the bug to be fixed.
- All code **must** follow its language's styling conventions.
- Use present tense (e.g. "Add feature" not "Added feature").
- Limit all lines to a maximum of 79 characters.

## Good Bug Reports

1. Don't open duplicate issues. Please search the existing issues before
opening a new one. Duplicate issues will be closed with a reference to the
original issue.
2. When filing a bug about exceptions or tracebacks, please include the
complete traceback. Without the complete traceback the issue might be
**unsolvable** and you will be asked to provide more information.

If the bug report is missing this information then it'll take us longer to fix
the issue. We will probably ask for clarification, and barring that if no
response was given then the issue will be closed.

## Starting

This guide assumes you have
[Git Flow](https://github.com/nvie/gitflow/wiki/Installation) installed on your
system. The `main` branch is **always** the production branch, and the
`develop` branch is **always** the development branch.

To create a feature/bugfix branch, use the command:

```sh
git flow feature start <feature-name>
# or
git flow bugfix start <bugfix-name>
```

Git Flow will automatically create and checkout the branch, make the changes in
your favorite code editor. When you're done with the changes, commit and use
the following command to publish the feature on GitHub:

```sh
git flow feature publish <feature-name>
# or
git flow bugfix publish <bugfix-name>
```

The branch should automatically be published on GitHub. Wait a supervisor to
review your code and merge or request changes if necessary.
