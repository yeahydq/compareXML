http://localhost:8080/jnlpJars/jenkins-cli.jar
http://localhost:8080/jnlpJars/jenkins-cli.jar

http://localhost:8080/me/configure

java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 help
java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin help

java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin list-jobs


freestyle
java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin delete-job freestyle_copy
java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin copy-job freestyle freestyle_copy
java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin build freestyle_copy

#+++++++++++++++++++++++++++++++++++++++++
# Create a jenkin job when there require new a branch
#+++++++++++++++++++++++++++++++++++++++++
curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -X get http://localhost:8080/job/freestyle/config.xml -o mylocalconfig.xml
curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -X POST http://localhost:8080/createItem?name=freestyle_new_1 --data-binary @mylocalconfig.xml -H "Content-Type:text/xml"
curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -X POST http://localhost:8080/job/freestyle_new_1/build --data-urlencode json='{"parameter": [{"name":"id", "value":"123"}, {"name":"verbosity", "value":"high"}]}'
# get the branch's create time
git log -n 1 remotes/master --format=format:%ci
git log remotes/master --format=format:%ci | tail

#+++++++++++++++++++++++++++++++++++++++++
# Compare the  git repos, and show the conflict item
#+++++++++++++++++++++++++++++++++++++++++
# list remote branch
git ls-remote https://github.com/yeahydq/compareXML
# or
git branch -r

# add remote
git remote add remotes https://github.com/pycontribs/jenkinsapi.git
# show remotes
git ls-remote remotes | grep heads

# compare 2 branch's commit, and show the ID
git fetch remotes
git log remotes/master --oneline | head
git log remotes/pytest --oneline | head
git log --left-right --graph --cherry-pick --oneline remotes/master...remotes/pytest

# show the change in a commit
git diff-tree --no-commit-id --name-only -r 4930e3c

#+++++++++++++++++++++++++
# add a tag
#+++++++++++++++++++++++++
git tag -a v1.01 -m "Relase version 1.01"

echo "dick" > dick1.txt
git add dick1.txt
git commit -m "`date`"

git tag -a v1.02 -m "Relase version 1.02"
git tag -a v1.03 -m "Relase version 1.03"

# show tags:
git tag

# show the commits between 2 tag
git log --pretty=oneline v1.01...v1.02
git log --pretty=oneline v1.01...v1.03

git diff-tree --no-commit-id --name-only -r 285bf
git diff-tree --no-commit-id --name-only -r 0fafb

# show the changes per file for the commits
git show 326505e2
# next -- how to push the tag into remote GIT HUB?
git push origin --tags


# how to auto create the pull request?


# Flow:
project <BASEL>
Step 1. Script to create a new brach and new jenkins jobs
BranchName: <BASEL>
Dev Env:
/hsbc/rpm/git/<basel>_ut/
/hsbc/rpm/git/<basel>_sit/ (cannot change rpm01exe)
Jenkins job:
GIT_WATCH_<BASEL> <- PIPELINE_<BASEL>

For GIT_WATCH_<BASEL>: Monitor any push on the <BASEL> branch

For PIPELINE_<BASEL>:
<preparation>
1. check if remote path exist, if not then fetch all from GITHUB, and create folder in DS/SAS server
2.       if remotem path exist,
git init
git remote add remotes https://github.com/pycontribs/jenkinsapi.git
git fetch remotes

for cmtId in `git log --right-only --graph --cherry-pick --oneline remotes/master...remotes/pytest | awk '{print $2}'`
do
    git diff-tree --no-commit-id --name-only -r $cmtId

done | sort | uniq
etl.list
sas.list
datastage.list
cat etl.list | xargs -n1 tar -cvf - | bzip2 > etl.tar
cat sas.list | xargs -n1 tar -cvf - | bzip2 > sas.tar
<Deploy>
scp etl.tar uat-basel.hsbc:/hsbc/rpm/git/xxx/etl.tar
scp sas.tar uat-basel.hsbc:/hsbc/rpm/git/xxx/sas.tar

ssh tar -xvf uat-basel.hsbc:/hsbc/rpm/git/xxx/etl.tar
ssh tar -xvf uat-basel.hsbc:/hsbc/rpm/git/xxx/sas.tar

https://jenkins.io/doc/pipeline/examples/

