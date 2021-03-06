
node {
   stage('Preparation') { // for display purposes
//  sh "rm -rf .git"
    checkout([$class: 'GitSCM', branches: [[name: '*/master']], userRemoteConfigs: [[credentialsId: 'eca4cce5-7e88-48de-b37e-7df5a2433385', url: 'git@github.com:yeahydq/compareXML.git']]])

    sh 'pwd'
        sh "echo 'preparation stage'"
        sh "git push origin regression"
        //  sh '''
        //  pwd
        //  git init
        //  git remote add remotes git@github.com:yeahydq/compareXML.git
        //  git pull
        //  '''
    }
   stage('Build') {
      // Run the maven build
        sshagent(['2b1204ba-55ed-42da-b682-e7903df9ed68']) {
            sh '''
            ssh -o StrictHostKeychecking=no dick@localhost "hostname;pwd;whoami;"
            '''
        }
   }
   stage('Results') {
      if (isUnix()) {
         sh "echo 'result stage'"
         sh '''
         whoami
         hostname
         '''
         sh "sleep 10"
      }

   }
}
