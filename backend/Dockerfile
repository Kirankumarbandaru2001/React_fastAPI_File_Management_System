# Step 1: Use the official Python image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the backend code to the container
COPY ./app /app

# Step 5: Expose the port FastAPI will run on
EXPOSE 8000

# Step 6: Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
