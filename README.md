Tag Table
=====

This is a _genericized_ version of a project:
Any revealing data has been modified or removed

The primary purpose of this repository as such thus is as a Proof of
Concept for an API used to __query and post test results as part of a
team's CI/CD__.

The API uses three points of reference to identify a build:
 * The SHA1 hash in GIT of the commit being tested
 * The name of the job/testsuite
 * The Environment Control List with which tests were run

Builds can query the API before starting to determine if another build is
necessary. Likewise after regression testing, a pass or fail result should
be POSTed as appropriate.
