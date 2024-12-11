FROM jenkins/jenkins:lts

# Switch to root to install Docker
USER root

# Install Docker
RUN apt-get update && \
    apt-get install -y docker.io && \
    usermod -aG docker jenkins

# Switch back to jenkins user
USER jenkins