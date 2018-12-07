Contributing guidelines
=======================

# Branches
PASDAC has two important branches, **master** and **development**. The **master** branch is intended to always be in working order. Code in this branch is tested and tried. Code in the development is freshly coded and tested updates, bug fixes, and new contributions that **work**. All other feature branches are for each member to experiment with, work on, fix bugs, and contribute new code to the library.

# Let's keep it simple for PASDAC

Generally:
- Branch off `development` and create a feature branch under your name to do you local work
- Make changes and commit your changes frequently
- Make sure changes are consistent with the HAbits Lab [Coding Style](https://drive.google.com/open?id=1Ne8g_nWbiyg5-GJ5NfPpWlUVnSPmtLI-CTTTXO0NI-k)
- Schema for storing data in our databases: [JSON data structure](https://drive.google.com/open?id=1KvyzyS0nrN__LWOn_R2D8JSXzI7p0eI8fm3WaaywIJY)
- Do a  [pull request](https://help.github.com/articles/about-pull-requests/) (this action will trigger a code review) when you are ready to merge back into development.

## Update your branch from _development_
Do this so that you local branch doesn't deviate too much from the _development_ branch. On the command line [do](https://stackoverflow.com/questions/16329776/how-to-keep-a-git-branch-in-sync-with-master)
> git checkout master
  git pull
  git checkout mobiledevicesupport
  git merge master
