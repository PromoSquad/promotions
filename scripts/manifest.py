import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
MANIFEST_PATH = os.path.join(PROJECT_DIR, 'manifest.yml')

MANIFEST_TEMPATE = """
---
# This manifest deploys a Python Flask application
applications:
  - name: {APP_NAME}
    path: .
    instances: 1
    memory: 256M
    routes:
      - route: {APP_NAME}.us-south.cf.appdomain.cloud
    disk_quota: 1024M
    buildpacks:
      - python_buildpack
    timeout: 180
    env:
      FLASK_APP: service:app
      FLASK_DEBUG: false
"""

APP_NAME = os.getenv('APP_NAME', 'nyu-promotion-service-fall2103-dev')

def main():
    print("Creating manifest file...")
    print("=== {} ===".format(MANIFEST_PATH))
    print(MANIFEST_TEMPATE.format(APP_NAME=APP_NAME))
    manifest = MANIFEST_TEMPATE.format(APP_NAME=APP_NAME)
    # write to MANIFEST_PATH
    with open(MANIFEST_PATH, 'w') as f:
      f.write(manifest)
    print("=== Done ===")

if __name__ == '__main__':
  main()
