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

curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -X get http://localhost:8080/job/freestyle/config.xml -o mylocalconfig.xml
curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -XPOST http://localhost:8080/createItem?name=freestyle_new_1 --data-binary @mylocalconfig.xml -H "Content-Type:text/xml"
curl -u dick:f8b6adb2c39ff087ac5b9e07f3b5933a -X POST http://localhost:8080/job/freestyle_new_1/build --data-urlencode json='{"parameter": [{"name":"id", "value":"123"}, {"name":"verbosity", "value":"high"}]}'

