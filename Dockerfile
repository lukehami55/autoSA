# Use the official Python image as the base image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the local files into the container's working directory
COPY localPopup.py /app/localPopup.py
COPY localAutomation.py /app/localAutomation.py
COPY autoindex.py /app/autoindex.py
COPY calckpi.py /app/calckpi.py

# Install tkinter (necessary for running the GUI)
RUN apt-get update && apt-get install -y python3-tk

# Install required Python packages
RUN pip install pandas

# Define the command to run when the container starts
CMD ["python", "localPopup.py"]
