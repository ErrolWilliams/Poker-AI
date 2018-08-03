# Poker-AI
Bot that plays poker and uses machine learning to become a better player (hopefully)

Make sure you have Python 3.6.5 or greater installed, then run setup_environment.py as superuser to install the required modules!
Running the code
```sh
$ python3 Poker-AI.py --help
(lists all options)

$ python3 Poker-AI.py --stats
(run as stats bot)

$ python3 Poker-AI.py -t --stats -p george
(run on training server as stats bot with playername george)
```
<pre>
Workflow
  Update local repo
    - git checkout master
    - git pull origin master
  Create working branch
    - git checkout -b WORKING_BRANCH
  Make changes on WORKING_BRANCH
  Add and commit changes once satisfied
    - git add /files/you/changed
    - git commit -m "Message describing changes"
  Push changes to master
    - git checkout master
    - git pull origin master
    - git merge WORKING_BRANCH
    - git push origin master
</pre>
