# Python API Service
FROM python:3.11.4-slim
WORKDIR /app
# First copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Then copy the rest of the code
COPY main.py .
CMD ["python", "main.py"]
