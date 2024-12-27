import os
import time
import base64
from kubernetes import client, config
from github import Auth
from github import Github
from github import GithubIntegration

# Initialize Kubernetes client
config.load_incluster_config()
v1 = client.CoreV1Api()

# GitHub authentication details
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
GITHUB_INSTALLATION_ID = os.getenv('GITHUB_INSTALLATION_ID')
GITHUB_PRIVATE_KEY_PATH = os.getenv('GITHUB_PRIVATE_KEY')  # Private key for GitHub App

# Load the private key
with open(GITHUB_PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()

# Generate GitHub installation token
def get_github_token():
    github = GithubIntegration(GITHUB_APP_ID, private_key)
    installation = github.get_app_installation(GITHUB_INSTALLATION_ID)
    token = github.get_access_token(installation.id)
    return token.token

# Function to update the Kubernetes secret with the new token
def update_secret(token):
    secret_name = "videopoint-ghcr-auth"
    secret_namespace = "default"
#    secret = v1.read_namespaced_secret(secret_name, secret_namespace)
#    secret.data['password'] = base64.b64encode(token.encode('utf-8')).decode('utf-8')
#    v1.replace_namespaced_secret(secret_name, secret_namespace, secret)
    data = {
            'password': base64.b64encode(token.encode('utf-8')).decode('utf-8'),
            'username': base64.b64encode(GITHUB_APP_ID.encode('utf-8')).decode('utf-8')
            }
    body = client.V1Secret()
    body.api_version = 'v1'
    body.data = data
    body.kind = 'Secret'
    body.metadata = {'name': secret_name, 'namespace': secret_namespace}
    body.type = 'Opaque'
    v1.create_namespaced_secret(secret_namespace, body)

print("Fetching new GitHub token...")
token = get_github_token()
print("Updating Kubernetes secret...")
update_secret(token)
print("Token updated.")
