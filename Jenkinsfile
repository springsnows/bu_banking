pipeline {
    agent any

    environment {
        // Name of the virtual environment directory.
        VENV = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                // Check out the source code.
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                // Create a virtual environment and upgrade pip.
                sh 'python -m venv ${VENV}'
                sh '. ${VENV}/bin/activate && pip install --upgrade pip'
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install the dependencies listed in requirements.txt.
                sh '. ${VENV}/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Apply Migrations') {
            steps {
                // Apply Django database migrations.
                sh '. ${VENV}/bin/activate && python manage.py migrate'
            }
        }
        stage('Run Tests') {
            steps {
                // Run Django tests.
                sh '. ${VENV}/bin/activate && python manage.py test'
            }
        }
        stage('Collect Static Files') {
            steps {
                // Collect static files (if applicable).
                sh '. ${VENV}/bin/activate && python manage.py collectstatic --noinput'
            }
        }
    }
    
    post {
        always {
            // Optionally archive static files or test reports.
            archiveArtifacts artifacts: 'staticfiles/**', allowEmptyArchive: true
        }
        failure {
            echo 'Build failed. Please check the logs for more details.'
        }
    }
}

