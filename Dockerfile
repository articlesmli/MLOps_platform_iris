FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN groupadd -g 1000 appuser && useradd -u 1000 -g appuser -s /bin/bash appuser

# Copy and install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model artifacts with proper permissions
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser models/ ./models/

# Switch to non-root user for execution
USER appuser

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]