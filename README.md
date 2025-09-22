# coding_challenge
Coding Challenge

First step: Extraction of software requirements

The PDF of the challenge was well structured to easily extract the requirements.
	- Web service that implements API endpoints (POST and GET)
	- Adaptable status code for API Call (Respond of 202 Accepted in POST Method)
	- Response of API Endpoints in .json format
	- Possibility of concurrent requests for summarazation and not to exceed 1500 characters
	- LLM - persistent and local Ollama instance running Gemma3:1B
	- Python 3.12 and delivered as pre-built Docker containers
	- API Specification - OpenAPI
	- Docker containers via DockerHub
	- optional: Uniqueness and re-summarazation
	
	Put this requirements into the different domains i.e:
	Backend/Webservice
	Infrastructure
	Documentation
	
	I am using a Client-Server Architecture with two microservices.
	
Second step: Research of pre-designed solutions/frameworks that solve a lot of the requirements
			 or at least simplify the new development for the challenge
			 
    For the backend/webservice:
	FastAPI is predestined for solving or simplify these requirements:
		- Web service that implements API endpoints (POST and GET)
		- Adaptable status code for API Call (Respond of 202 Accepted in POST Method)
		- Response of API Endpoints in .json format
		- uses Python
		
	Infrastructure:
	Docker for development of persistent and deployable containers/images:
		- LLM - persistent and local Ollama instance running Gemma3:1B
		- Docker containers via DockerHub
		
	Documentation:
	FastAPI for API specification
		- API Specification in OpenAPI

Third step: Creation of first project structure
	Divide Ollama and FastAPI Code
	app directory for FastAPI main.py
	storage for persistent saving and loading of documents
	models for saving the ollama gemma3:1b model
	tests for test code
	docker-compose.yml to orchestrate the usage of the FastAPI App and the Ollama model
	requirements.txt for the requirements
	Dockerfile for the FastAPI App
	Another Dockerfile for the Ollama Server in the models directory
	
Fourth step: Research of existing Dockerfiles or input for FastAPI and Ollama
	The providers of the frameworks generally have documentation about containerization of their frameworks i.e:
	https://fastapi.tiangolo.com/deployment/docker/?h=docker
	
	Adaptation of the Dockerfiles
	
	Create Docker images for both FastAPI App and Ollama Server
	
	Use docker compose up to build the infrastructure
	
	Gemma3:1b was installed via ollama pull gemma3:1b after Ollama Server was running
	This model was locally installed under ./models/ollama/models
	
	After this step the image is built to provide the Ollama Server and the gemma3:1b model
	
Fifth step: Design of Python code with FastAPI
	
	Me as a user wants to have persistent document data. I want to load/save the content of the document, so
	I build to methods for these cases.
	
	FastAPI also includes pydantic, so I can use the BaseModel to determine that the inputs should always have these
	data types.
	
	I created two classes: SummarizerInput (POST Method) and SummarizerDocument to save and load the document content
	with a validation of the data types.
	
	For concurrent requests I use a asynchronized background task that execute the summarazation for different documents.
	
	The example to use gemma3:1b is from https://github.com/ollama/ollama-python/blob/main/examples/async-generate.py.
	
	Tests were made with ChatGPT.
	
Sixth step: Deployment of the docker container on DockerHub
	After intense testing the docker images are deployed on DockerHub:
	
	https://hub.docker.com/repository/docker/projectdc95/coding_challenge-ollama/general
	and
	https://hub.docker.com/repository/docker/projectdc95/coding_challenge-fastapi/general			 


Optional:
Scalability & Robustness:
Demonstrate how your design could handle high load and recover from errors.
Your documentation should justify the architectural patterns and technologies
you chose to achieve this.

First of all I would suggest a real server like nginx/Apache in a production mode, because uvicorn is just a
ASGI-Server (.Asynchronous Server Gateway Interface).

This would be an ideal Kubernetes Use-Case with the possibility to create replicas of the Docker Image Objects
and Self-Healing Mechanism. Also for High Load to use horizontal/vertical scaling to balance the load.