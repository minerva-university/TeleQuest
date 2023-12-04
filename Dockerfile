# Use a multi-stage build to build the frontend
# Stage 1: Build the frontend
FROM node:16 as frontend-builder
WORKDIR /app

# Copy the frontend application to /app
COPY web/ /app/web/

# Install dependencies and build your application
WORKDIR /app/web
RUN npm install
RUN npm run build


# Stage 2: Set up the Python environment
FROM python:3.11-slim
WORKDIR /app

# Install Node.js in the Python image
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Copy the Python requirements and install them
COPY mypy-requirements.txt .
COPY .env .
COPY utils.py .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r mypy-requirements.txt

# Copy the necessary directories to the Docker image
COPY ai ai/
COPY bot bot/
COPY db db/

# Copy the main application file
COPY app.py .

# Copy the built frontend assets from the frontend-builder stage
COPY --from=frontend-builder /app/web/build /app/web/build

# The command to run the app
CMD ["python", "app.py"]