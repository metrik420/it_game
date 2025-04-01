FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Ensure that /app is in the Python path so modules are found
ENV PYTHONPATH=/app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose container port 5000
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
