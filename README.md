# General info

There are some general rules that you should follow in this project:

1. Communicate!  Use the tools at your disposal to inform the other members of the team of your progress, the issues that you are tackling, and what you are working on at the moment.

2. Really, communicate!

3. Do not “push” buggy code to the remote master branch; always do extensive testing before pushing a major upgrade in the code. — always ask for someone to cross-check your code when uploading major changes by making a pull-request. After the pull request has been made, the reviewer is responsible for merging the branch into the master.

  3.a) if the code can not be automatically merged, the creator of the pull request should resolve all the conflicts, first.

4. Ensure modularity of your code.

5. Ensure scalability: do not hardcode any parts of your code.

## Communication
Communication will be done via two ways:

1. issue a ticket in Git (look on the right side bar for “Issues”)

2. write an e-mail (either to everybody or just to the teaching assistant).

The first one is preferred given that it’s easy to assign people that can work on the bug/enhancement/question and you can also close the issue when the problem has been fixed. 

## Git usage

To set up Git use a GUI based software such as, e.g, Sourcetree. There are numerous softwares like this for all platforms.

You can also do it via command line as follows:

  > mkdir /path/to/your/project
  >
  > cd /path/to/your/project
  >
  > git clone https://github.com/faitdivers/pyao.git

More information on how to commit, reset, branch, stage files, pull, etc. can be found in [git-scm.com/book/en/Git-Basics](http://git-scm.com/book/en/Git-Basics)

# Documentation
The Git repository will also work as a place to document our work and to communicate between one another. In the doc folder you can access different documents and edit them. The way to document the progress should be modular, but structured in such way that the links between each module of the simulator are clear.

__Important remark:__ The documentation is to be done in LaTex.

## Why not a wiki

Several wikis were tested; none of them were suitable for our project.

- [wikia.com](http://wikia.com "") -  free hosting but no support for LaTeX; everybody can see it and change it;
- [wiki.tudelft.nl](http://wiki.tudelft.nl "") - free hosting but incredibly slow; not active at all; no support for LaTeX; search engine is horrible; supports having users with different permissions though;
- *gitwiki* - there is a wiki embedded in the git repository; however it is very very simple and although only people with commit permissions can write on it it has no support for LaTeX formulas 	and other advanced document formatting tools.

A Wikimedia website would be prefered, but we have no host for that at the moment.
