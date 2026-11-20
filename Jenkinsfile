pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        APP_PORT = '5001'
        DEPLOY_DIR = 'deployment'
        VENV_DIR = "/tmp/flask-ci-${BUILD_TAG}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'BUILD: Creating a Python virtual environment and installing pinned dependencies'
                sh '''
                    set -eu
                    command -v python3
                    python3 -c 'import sys; assert (3, 12) <= sys.version_info[:2] < (3, 14), "Python 3.12 or 3.13 is required"'
                    env -u PYTHONHOME -u PYTHONPATH python3 -m venv --without-pip "$VENV_DIR"
                    site_packages=$("$VENV_DIR/bin/python" -c 'import sysconfig; print(sysconfig.get_path("purelib"))')
                    env -u PYTHONHOME -u PYTHONPATH python3 -m pip install --target "$site_packages" -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'TEST: Running automated unit tests'
                sh 'env -u PYTHONHOME -u PYTHONPATH "$VENV_DIR/bin/python" -m unittest -v test_app'
            }
        }

        stage('Deploy') {
            steps {
                echo 'DEPLOY: Copying the application into the deployment directory'
                sh '''
                    mkdir -p "$DEPLOY_DIR"
                    cp app.py requirements.txt "$DEPLOY_DIR"/
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'RUN: Starting the deployed Flask application'
                sh '''
                    if [ -f "$DEPLOY_DIR/app.pid" ]; then
                        old_pid=$(cat "$DEPLOY_DIR/app.pid")
                        if kill -0 "$old_pid" 2>/dev/null; then
                            kill "$old_pid"
                        fi
                        rm -f "$DEPLOY_DIR/app.pid"
                    fi

                    nohup env -u PYTHONHOME -u PYTHONPATH APP_PORT="$APP_PORT" \
                        "$VENV_DIR/bin/python" \
                        "$WORKSPACE/$DEPLOY_DIR/app.py" \
                        > "$WORKSPACE/$DEPLOY_DIR/app.log" 2>&1 \
                        < /dev/null &
                    echo $! > "$DEPLOY_DIR/app.pid"
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'VERIFY: Checking the deployed application over HTTP'
                sh '''
                    env -u PYTHONHOME -u PYTHONPATH APP_PORT="$APP_PORT" "$VENV_DIR/bin/python" - <<'PY'
import os
import time
import urllib.error
import urllib.request

url = "http://127.0.0.1:" + os.environ["APP_PORT"]
last_error = None

for attempt in range(15):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode("utf-8")
            print("HTTP Status:", response.status)
            print("Response Body:", body)
            if response.status != 200:
                raise AssertionError("Unexpected HTTP status: " + str(response.status))
            if body != "Hello, Jenkins Multi-Stage Pipeline!":
                raise AssertionError("Unexpected response body: " + repr(body))
        print("DEPLOYMENT VERIFICATION SUCCESSFUL")
        break
    except (OSError, urllib.error.URLError) as error:
        last_error = error
        if attempt == 14:
            raise RuntimeError("Deployed application did not become ready") from last_error
        time.sleep(1)
PY
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'FAILURE: CI/CD pipeline failed; later stages were not run.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
