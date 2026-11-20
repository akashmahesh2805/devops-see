
pipeline {
    agent any

    environment {
        APP_PORT = '5001'
        DEPLOY_DIR = 'deployment'
    }

    stages {

        stage('Build') {
            steps {
                echo 'BUILD: Creating environment and installing dependencies'

                sh '''
                    /usr/bin/python3 -m venv .venv

                    .venv/bin/python -m pip install --upgrade pip

                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'TEST: Running automated unit tests'

                sh '''
                    .venv/bin/python -m unittest -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'DEPLOY: Copying application to deployment directory'

                sh '''
                    mkdir -p "$DEPLOY_DIR"

                    cp app.py requirements.txt "$DEPLOY_DIR"/
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'RUN: Starting deployed Flask application'

                sh '''
                    if [ -f "$DEPLOY_DIR/app.pid" ]; then
                        kill "$(cat "$DEPLOY_DIR/app.pid")" 2>/dev/null || true
                        sleep 1
                    fi

                    nohup "$WORKSPACE/.venv/bin/python" \
                        "$WORKSPACE/$DEPLOY_DIR/app.py" \
                        > "$WORKSPACE/$DEPLOY_DIR/app.log" 2>&1 \
                        < /dev/null &

                    echo $! > "$DEPLOY_DIR/app.pid"
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'VERIFY: Testing deployed Flask application'

                sh '''
                    APP_PORT="$APP_PORT" .venv/bin/python - <<'PY'
import os
import time
import urllib.request

url = "http://127.0.0.1:" + os.environ["APP_PORT"]

for attempt in range(15):
    try:
        response = urllib.request.urlopen(url, timeout=3)

        body = response.read().decode("utf-8")

        print("HTTP Status:", response.status)
        print("Response Body:", body)

        assert response.status == 200
        assert body == "Hello, Jenkins Multi-Stage Pipeline!"

        print("DEPLOYMENT VERIFICATION SUCCESSFUL")
        break

    except Exception as error:
        if attempt == 14:
            raise
        time.sleep(1)
PY
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'FAILURE: CI/CD pipeline failed. Check the console output.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
