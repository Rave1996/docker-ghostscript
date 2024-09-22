FROM python:3.12.6-alpine3.20

# Install Ghostscript
RUN apk add ghostscript

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
