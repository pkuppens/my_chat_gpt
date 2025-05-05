FROM ollama/ollama:latest

# Install extra CLI tools and shells
RUN apt-get update && apt-get install -y \
    vim \
    zsh \
    csh \
    curl \
    git \
    htop \
    && apt-get clean

# Set default shell (optional)
SHELL ["/bin/zsh", "-c"]

# Ensure the .ollama directory exists and has proper permissions
RUN mkdir -p /root/.ollama && chmod 755 /root/.ollama

# Explicitly set the entrypoint to ensure Ollama starts properly
ENTRYPOINT ["ollama", "serve"]
