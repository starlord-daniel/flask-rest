# In the first part of our Dockerfile, we define the base Docker Image we want to use for the container.
FROM alpine:latest

# We add Python to our Docker Image
RUN apk add --no-cache python3 && \ 
                        python3 -m ensurepip && \
                        rm -r /usr/lib/python*/ensurepip && \
                        pip3 install --upgrade pip setuptools && \ 
                        if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \ 
                        if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \ 
                        rm -r /root/.cache
RUN apk add --update python3 python3-dev
RUN apk add gfortran \
            build-base \
            openssl-dev \
            openblas \
            libc-dev \
            gcc \
            libffi-dev \
            build-base \
            ca-certificates \
            jpeg-dev \
            openjpeg-dev \
            lapack \
            lapack-dev

# move data to the image. Left is location on your machine, right is location in the container
COPY requirements.txt requirements.txt
COPY . .

# Install app dependencies - rerun when you edit requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for container accessibility. You still have to add -p 8000:8000 to the docker run command
EXPOSE 8000
ENTRYPOINT ["python"]

# start the app.py file 
CMD ["run.py"]