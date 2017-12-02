# flask-rest
A RESTful service based on the Flaks Python framework

## Docker Container 
The Create an image from the Flask service and run it and upload it as a web service, follow these steps:

1. Build the image by running:
    ```docker
    docker build -t <image-name> .
    ```

    Where -t is used to set the tag for the image to create. The dot (.) at the end refers to the file path of the Dockerfile. For the build to work, the whole path can't contain any spaces. Something like C:\test would be fine, but "C:\test\this app" wouldn't be.

    An example: 

    ```docker
    docker build -t flask-rest .
    ```

2. Run the container locally:
    ```docker
    docker run -p 8000:8000 <image-name>
    ```

    The property -p sets the port mapping for the container. As the script exposes port 8000, this should be mapped to another port of the container. You might change the second value (right) to change the port to speak to. 

    An example: 

    ```docker
    docker run -p 8000:8000 flask-rest
    ```