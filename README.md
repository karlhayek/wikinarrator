# Wiki Narrator


<p align="left">
<img src="frontend/src/assets/wikinarrator_logo.jpg" width=150>
</p>

Project that retrieves cleaned text from Wikipedia articles and sends them to a TTS service (Azure's speech studio, Deepzen, etc.)


## Building and running with Docker
Note: [Install Docker](https://docs.docker.com/get-docker) first.
* Start the stack with Docker Compose:
```
docker-compose -f docker-compose.yml up
```
* Docker will build and run the images according to `docker-compose.yml`, and you will be able to interact with the following URLs:

The Frontend, a [Vue.js](https://vuejs.org/) application served using [Nginx](https://www.nginx.com/): https://localhost

The Backend, a Python server using the [FastAPI](https://fastapi.tiangolo.com/) framework: https://localhost/api/

[Traefik](https://containo.us/traefik/) UI, to see how the routes are being handled by the reverse proxy (only available in development mode, described below): http://localhost:8080.

Note that in production (default) mode all the above routes use HTTPS, with Traefik redirecting all incoming HTTP traffic to HTTPS. In development mode, the routes use HTTP.


#### Jupyter

Additionally, this enables you to use [Jupyter Notebook](http://jupyter.org/) from inside the backend container. First enter  the running Docker container:

```
docker-compose exec backend bash
```

Then enter the commmand: `$JUPYTER`. This starts a Jupyter Lab session configured to listen on the public port, so you can open and use it from your browser. Since it is running inside the container, it has direct access to the database by the container name, etc. So, you can just copy your backend code and run it directly, without needing to modify it.

#### Restart an individual container
```
docker-compose up --build --no-deps -d <image-name>
```
This is useful if you want to rebuild an image without restarting other  containers that are already running.
For example, if you want to rebuild the backend image in the development stack because you changed the backend dockerfile or added a Python package in `requirements.txt`, run:
```
docker-compose -f docker-compose.dev.yml up --build --no-deps -d backend
```
