FROM python

# Set working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "main.py"]
