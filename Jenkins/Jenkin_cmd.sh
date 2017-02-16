http://localhost:8080/jnlpJars/jenkins-cli.jar
http://localhost:8080/jnlpJars/jenkins-cli.jar

http://localhost:8080/me/configure

java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 help
java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin help

java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin list-jobs


freestyle
dick@:~/.ssh$ java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin delete-job freestyle_copydick@:~/.ssh$ java -jar /dick/tool/jenkins_tool/jenkins-cli.jar -s http://localhost:8080 -i /home/dick/.ssh/key_for_jenkin copy-job  freestyle freestyle_copy
