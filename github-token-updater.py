import os
import time
from kubernetes import client, config
from github import Github  # Install PyGithub via pip

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

# Generate GitHub installation token (example)
def get_github_token():
    # Use PyGithub or another method to get the token
    github = Github(app_id=GITHUB_APP_ID, private_key)
    installation = github.get_installation_by_id(GITHUB_INSTALLATION_ID)
    token = installation.get_access_token()
    return token.token

# Function to update the Kubernetes secret with the new token
def update_secret(token):
    secret_name = "github-ghcr-secret"
    secret_namespace = "default"

    secret = v1.read_namespaced_secret(secret_name, secret_namespace)
    secret.data['password'] = token
    v1.replace_namespaced_secret(secret_name, secret_namespace, secret)

print("Fetching new GitHub token...")
token = get_github_token()
print("Updating Kubernetes secret...")
update_secret(token)
print("Token updated.")
