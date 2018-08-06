# Poker-AI
Bot that plays poker and uses machine learning to become a better player (hopefully)

Make sure you have Python 3.6.5 or greater installed, then run setup_environment.py as superuser to install the required modules!
#### Running the code
```sh
$ ./Poker-AI.py --help
(lists all options)

$ ./Poker-AI.py server stats
(run on game server as stats bot)

$ ./Poker-AI.py practice stats --name george
(run on practice server as stats bot with playername george)

$ ./Poker-AI.py practice bot --load basicPlayer1 --name george
(run on practice server as old-style bot with model basicPlayer1 and player name george)
```
#### Workflow
<pre>
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
