FROM jenkins/jenkins:lts

# Install Docker inside Jenkins for agent control (optional)
USER root
RUN apt-get update && apt-get install -y \
    docker.io \
    git \
    python3 \
    python3-pip && \
    apt-get clean

# Set permissions
RUN usermod -aG docker jenkins

USER jenkins
