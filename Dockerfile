FROM python:3.12.6-slim

# Install Ghostscript
RUN apt-get update && apt-get install -y ghostscript

# Establish working dir
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Deploy 5000 port
EXPOSE 5000

# Execute gunicorn with 2 workers
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
