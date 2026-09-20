FROM python:3.11-slim

# Copy the local codebase into the container
COPY . /app
WORKDIR /app

# Install the agent-review-graph package globally
RUN pip install --no-cache-dir .

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# GitHub Actions overrides the working directory to the user's workspace at runtime
ENTRYPOINT ["/entrypoint.sh"]
