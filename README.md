# Poker-AI
<pre>
Bot that plays poker and uses machine learning to become a better player (hopefully)

Run setup_environment.py as superuser to install the required modules!

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
Running the code
'''sh
$ python3 Poker-AI.py --help

$ python3 Poker-AI.py --stats

$ python3 Poker-AI.py -t --stats -p george
'''

1. (lists all options)
2. (run as stats bot)
3. (run on training server as stats bot with playername george)
