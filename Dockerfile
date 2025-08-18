FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libudev1 \
    libx11-6 \
    libxcursor1 \
    libxrandr2 \
    libxi6 \
    libxinerama1 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY run.sh .
COPY main.py .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install open3d numpy matplotlib tqdm

RUN chmod +x run.sh

CMD ["bash"]
