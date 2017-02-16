!groovy
# http://www.tuicool.com/articles/aUriAfy

node {
   def mvnHome
   stage('Preparation') { // for display purposes
      if (isUnix()) {
         sh "echo 'preparation stage'"
         sh "sleep 2"
      } else {
         bat(/"${mvnHome}\bin\mvn" -Dmaven.test.failure.ignore clean package/)
      }
   }
   stage('Build') {
      // Run the maven build
      if (isUnix()) {
         sh "echo 'build stage'"
         sh "sleep 5"
      } else {
         bat(/"${mvnHome}\bin\mvn" -Dmaven.test.failure.ignore clean package/)
      }
   }
   stage('Results') {
      if (isUnix()) {
         sh "echo 'result stage'"
         sh "sleep 10"
      } else {
         bat(/"${mvnHome}\bin\mvn" -Dmaven.test.failure.ignore clean package/)
      }
   }
}
