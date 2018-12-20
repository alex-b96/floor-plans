Command line instructions

Git global setup
git config --global user.name "Irinel Bogdan"
git config --global user.email "irinel@falcontrading.ro"

Create a new repository
git clone git@git.falcon.zone:siteonline/2-measure.it.git
cd 2-measure.it
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

Existing folder
cd existing_folder
git init
git remote add origin git@git.falcon.zone:siteonline/2-measure.it.git
git add .
git commit -m "Initial commit"
git push -u origin master

Existing Git repository
cd existing_repo
git remote rename origin old-origin
git remote add origin git@git.falcon.zone:siteonline/2-measure.it.git
git push -u origin --all
git push -u origin --tags