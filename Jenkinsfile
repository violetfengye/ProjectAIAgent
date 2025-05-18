pipeline {
    agent any  // 在任何可用节点运行
    stages {
        stage('Build') {
            steps {
                // 替换为你的实际构建命令（例如 Maven/NPM/Shell）
                bat 'echo "开始构建..."'
                bat'make build'  // 示例命令
            }
        }
        stage('Test') {
            steps {
                bat 'echo "运行测试..."'
                bat 'npm test'     // 示例命令
            }
        }
    }
}