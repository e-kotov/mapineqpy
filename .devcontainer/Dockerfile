FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Quarto
# Using a specific version for reproducibility, but can be updated.
ARG QUARTO_VERSION=1.6.39
RUN curl -o quarto.deb -L https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb \
    && dpkg -i quarto.deb \
    && rm quarto.deb

# Set up working directory
WORKDIR /workspace

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --all-extras

# Clean up
RUN uv cache clean

# Add .venv bin to path so we don't need to activate
ENV PATH="/workspace/.venv/bin:$PATH"

CMD ["/bin/bash"]
