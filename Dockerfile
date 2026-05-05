FROM python:3.13-slim

# Install system dependencies, gnupg, and curl with retry logic
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends gnupg2 curl apt-transport-https ca-certificates && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV FLASK_APP=webapp.py
ENV FLASK_ENV=development

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
