FROM python:3.9-slim

# Install dependencies
RUN pip install kubernetes PyGithub

# Copy the Python script into the container
COPY github-token-updater.py /usr/src/app/github-token-updater.py

# Set environment variables (you can also pass them at runtime)
#ENV GITHUB_APP_ID=
#ENV GITHUB_INSTALLATION_ID=
#ENV GITHUB_PRIVATE_KEY_PAT=/github-app-key.pem

# Set the working directory
WORKDIR /usr/src/app

# Run the script
CMD ["python", "update_github_token.py"]
