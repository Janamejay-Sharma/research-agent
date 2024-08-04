# Setup
### Prerequisites:
Weaviate's `connect_to_embedded()` is an experimental feature and does not seem to work with a locally running Flask app. Instead we will have to deploy Weaviate with Docker.  

1. Set up Docker and Docker Compose: https://weaviate.io/blog/docker-and-containers-with-weaviate

2. Further instructions for Weaviate and Docker Compose: https://weaviate.io/developers/weaviate/installation/docker-compose

### Running the app:
1. Ensure that the Docker daemon is running:
    ```
    dockerd
    ```
1. To start your Weaviate instance, run this command in your shell:
    ```
    docker compose up weaviate
    ```
1. Run the Flask app:
    ```
    python3 app.py
    ```