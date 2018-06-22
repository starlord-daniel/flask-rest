# In the first part of our Dockerfile, we define the base Docker Image we want to use for the container.
# Ubuntu 16.04
FROM ubuntu:16.04

ARG CNTK_VERSION="2.5.1"
LABEL maintainer "MICROSOFT CORPORATION" \
      com.microsoft.cntk.version="$CNTK_VERSION"

ENV CNTK_VERSION="$CNTK_VERSION"

# Install CNTK as the default backend for Keras
ENV KERAS_BACKEND=cntk

RUN apt-get update && apt-get install -y --no-install-recommends \
    # General
        python3-pip \
        python3-setuptools \
        libpython3-dev \
        ca-certificates \
        wget \
        sudo \
        build-essential \
        && \
    # Clean-up
    apt-get -y autoremove \
        && \
    rm -rf /var/lib/apt/lists/*

# Get CNTK Binary Distribution
RUN CNTK_VERSION_DASHED=$(echo $CNTK_VERSION | tr . -) && \
    ([ "$CNTK_VERSION" != "2.4" ] || VERIFY_SHA256="true") && \
    CNTK_SHA256="386fe7589cb8759611d68a8ed8c888bf6b5dec3c3b2772c2c6a680ffe9fcce60" && \
    wget -q https://cntk.ai/BinaryDrop/CNTK-${CNTK_VERSION_DASHED}-Linux-64bit-CPU-Only.tar.gz && \
    ([ "$VERIFY_SHA256" != "true" ] || (echo "$CNTK_SHA256 CNTK-${CNTK_VERSION_DASHED}-Linux-64bit-CPU-Only.tar.gz" | sha256sum --check --strict -)) && \
    tar -xzf CNTK-${CNTK_VERSION_DASHED}-Linux-64bit-CPU-Only.tar.gz && \
    rm -f CNTK-${CNTK_VERSION_DASHED}-Linux-64bit-CPU-Only.tar.gz && \
    /bin/bash /cntk/Scripts/install/linux/install-cntk.sh --py-version 35 --docker

WORKDIR /root


# move data to the image. Left is location on your machine, right is location in the container
COPY requirements.txt requirements.txt
COPY . .

# Install app dependencies - rerun when you edit requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Expose port 8000 for container accessibility. You still have to add -p 8000:8000 to the docker run command
EXPOSE 8000
ENTRYPOINT ["python3"]

# start the app.py file 
CMD ["run.py"]