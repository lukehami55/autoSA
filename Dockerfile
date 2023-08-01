# Use the official Python image as the base image
FROM python:3

# Install X11 utilities and xvfb
RUN apt-get update && apt-get install -y x11-utils xvfb

# Set the working directory inside the container
WORKDIR /app

# Install required Python packages
RUN pip install pandas

# Copy the local files into the container's working directory
COPY localPopup.py /app/localPopup.py
COPY localAutomation.py /app/localAutomation.py
COPY autoindex.py /app/autoindex.py
COPY calckpi.py /app/calckpi.py

# Set the environment variables for xvfb
ENV DISPLAY=:99

# Start xvfb and run the Tkinter application
CMD ["xvfb-run", "-s", "-screen 0 1920x1080x24", "python", "localPopup.py"]
