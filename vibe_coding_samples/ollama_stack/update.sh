#!/bin/bash
set -e

# Function to log errors and exit
log_error() {
    echo "❌ Error: $1" >&2
    exit 1
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    log_error "Docker is not running. Please start Docker and try again."
fi

# Track current image digest before pull
current_digest=$(docker inspect --format='{{index .RepoDigests 0}}' ollama/ollama:latest 2>/dev/null || echo "")

echo "→ Pulling latest ollama image..."
if ! docker pull ollama/ollama:latest > /tmp/docker_pull_output.txt 2>&1; then
    log_error "Failed to pull ollama image. Check your internet connection and try again."
fi
echo "✅ Image pull completed successfully"

# Check new digest after pull
new_digest=$(docker inspect --format='{{index .RepoDigests 0}}' ollama/ollama:latest 2>/dev/null || echo "")

if [[ -z "$new_digest" ]]; then
    log_error "Failed to retrieve image digest. The image might not exist or there might be a network issue."
fi

# Check if we need to build the ollama-plus image
should_build_image=false
if [[ "$current_digest" != "$new_digest" || -z "$current_digest" ]]; then
    should_build_image=true
    echo "ℹ️ New base image detected or no existing image. Will build ollama-plus."
fi

# Check if ollama-plus image exists
if ! docker image inspect ollama-plus:latest > /dev/null 2>&1; then
    should_build_image=true
    echo "ℹ️  ollama-plus image not found. Will build it."
fi

if [[ "$should_build_image" == true ]]; then
    echo "→ Building ollama-plus image..."
    if ! docker-compose build ollama; then
        log_error "Failed to build ollama-plus image."
    fi
    echo "✅ ollama-plus image built successfully"
else
    echo "ℹ️ No need to rebuild ollama-plus image."
fi

# Check if we need to build the stack
should_build_stack=false
if [[ "$should_build_image" == true ]]; then
    should_build_stack=true
    echo "ℹ️ New image built, will rebuild stack."
fi

# Check if stack containers exist
if ! docker-compose ps ollama > /dev/null 2>&1; then
    should_build_stack=true
    echo "ℹ️ Stack containers not found. Will build and start the stack."
fi

if [[ "$should_build_stack" == true ]]; then
    echo "→ Building and starting stack..."
    if ! docker-compose up -d; then
        log_error "Failed to start stack."
    fi
    echo "✅ Stack started successfully"
else
    echo "ℹ️ No need to rebuild stack."
fi

echo "✅ Update complete."
