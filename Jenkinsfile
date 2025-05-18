pipeline {
    agent any  // 在任何可用节点运行
    stages {
        stage('Build') {
            steps {
                // 替换为你的实际构建命令（例如 Maven/NPM/Shell）
                sh 'echo "开始构建..."'
                sh 'make build'  // 示例命令
            }
        }
        stage('Test') {
            steps {
                sh 'echo "运行测试..."'
                sh 'npm test'     // 示例命令
            }
        }
    }
}