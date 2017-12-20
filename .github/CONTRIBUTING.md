We are glad that you decide to help us on this project.
Therefore, we would like to have some regulation, it's
not a long list, but will help us a lot.

### Coding Conventions

Since ImageButler is written on Python, therefore PEP8
is required for conventions. We also included PEP8 into 
the test, so you should check it before making a PR.

### Testing

Please also contribute with the tests, to improve ImageButler's
quality. All the PRs should pass the test on Travis before
getting acceptance.

### SMC and Versioning

#### Branches
* **master**: _master_ branch is the default branch of this repository. It's should be the source code of the main stable release.
* **R/x.x** (for example: _0.0_): branches for main versions, these branches should be protected and merged at every releases. Tagging should also be done in these branches.
* **R/x.x.x** (for example: _0.0.3_): branches for the sub release versions. Develop branches should be merged into these kind of branches. Sub release branches will be deleted at the end of the sub release.
* **D/x.x.x/{issue_number}*_{suffix}***: every develop branches should be indicated to one issue. Suffix should be added if you want to test with 3rd services (ex: Travis). _Develop branches should only be created at your forked repos._

#### Commits
* Every commits should have follow the following format (except merge commits)
```
[R/{milestone_version}/#{issue_number}] commit's contents
```
