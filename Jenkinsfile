pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = 'student-academic-platform'
        IMAGE_TAG  = 'v1.0.0'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
                sh 'git log --oneline -5 || true'
            }
        }

        stage('Verify Environment') {
            steps {
                sh 'java -version || true'
                sh 'git --version'
                sh 'python3 --version'
                sh 'python3 -m pip --version || true'
                sh 'docker --version || echo "Docker not available on agent"'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv-ci
                    .venv-ci/bin/python -m pip install --upgrade pip
                    .venv-ci/bin/python -m pip install -r requirements.txt pytest-cov
                    if [ -f requirements-dev.txt ]; then .venv-ci/bin/python -m pip install -r requirements-dev.txt; fi
                '''
            }
        }

        stage('Lint (non-blocking)') {
            steps {
                sh '''
                    .venv-ci/bin/python -m flake8 app tests --max-line-length=120 || echo "flake8 warnings (non-blocking)"
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    .venv-ci/bin/python -m pytest -v \
                        --junitxml=reports/jenkins-test-results.xml \
                        -o addopts=""
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'reports/jenkins-test-results.xml'
                    archiveArtifacts allowEmptyArchive: true,
                        artifacts: 'reports/jenkins-test-results.xml'
                }
            }
        }

        stage('Docker Build (if supported)') {
            steps {
                sh '''
                    if docker info >/dev/null 2>&1; then
                      docker build -t $IMAGE_NAME:$IMAGE_TAG .
                      docker images | grep $IMAGE_NAME || true
                    else
                      echo "Docker daemon not available on Jenkins agent - skipping image build."
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo 'All Jenkins pipeline stages completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
        always {
            echo "Build result: ${currentBuild.currentResult}"
        }
    }
}
