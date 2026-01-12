FROM python:3.12-slim-bookworm

# Install basic system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install Quarto
# Using a fixed version to ensure reproducibility, check https://github.com/quarto-dev/quarto-cli/releases for updates
ARG QUARTO_VERSION="1.6.40"
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "amd64" ]; then \
        QUARTO_ARCH="linux-amd64"; \
    elif [ "$ARCH" = "arm64" ]; then \
        QUARTO_ARCH="linux-arm64"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.deb \
    && dpkg -i quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.deb \
    && rm quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.deb

# Set the working directory
WORKDIR /workspace
