# ------------------------------
# Stage 1 - Base image for building and installing dependencies
# ------------------------------
FROM python:3.12-alpine AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.7.1

# Install dependencies for building
RUN apk add --no-cache gcc musl-dev libffi-dev build-base curl

# Create working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install runtime dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Stage 2 - Test image (optional)
# ------------------------------
FROM base AS test

COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# ------------------------------
# Stage 3 - Final runtime image
# ------------------------------
FROM python:3.12-alpine AS final

# Install runtime dependencies
RUN apk add --no-cache libffi

# Create a non-root user
RUN adduser -D appuser

# Set workdir
WORKDIR /app

# Copy installed dependencies from base
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy the application code
COPY app/ .

# Set permissions and switch to non-root user
RUN mkdir -p /app/logs && chown -R appuser /app
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs
RUN chown -R appuser /app && chmod -R u+rwX /app
USER appuser

# Expose FastAPI default port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
