
# Specifying base image
FROM python:3.9-slim

# set working directory
WORKDIR /app

# copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy rest of application code 
COPY . .

#exposing the port that FASTAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --port 8000 specifies the port
# The "main:app" refers to the 'app' object in 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

