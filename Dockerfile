#using python image as a parent image
FROM python:3.9-slim

#Installing system level dependencies 
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-opencv \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip3 install opencv-python 
RUN pip install --upgrade openpyxl

#setting working directory
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]


# sudo docker run -it   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix:/tmp/.X11-unix   automated_planogram python ./src/main.py
