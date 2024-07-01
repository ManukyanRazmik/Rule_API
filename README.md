# SMT Engine

SMT Engine is a FastAPI-based application for processing and comparing data from various sources. It supports report and comparison rules, providing flexibility in handling Inventory, Laboratory, and EDC datasets.

## Project Structure

```plaintext
smtengine_rules
  ├── config
  │    └── key_config.yaml
  ├── SMTEngine
  │    ├── Models
  │    │    └── RuleModels.py
  │    ├── Rules
  │    │    ├── Compare.py
  │    │    ├── Report.py
  │    │    └── __init__.py
  │    ├── utils
  │    │    ├── compare_utils.py
  │    │    ├── report_utils.py
  │    │    └── __init__.py
  │    ├── API.py
  │    └── __init__.py
  ├── .gitignore
  ├── Dockerfile
  ├── MANIFEST.in
  ├── requirements.txt
  └── setup.py
```

## Configuration
`main_config.yaml` This file contains the configuration settings used by the application.
## SMTEngine Package
`SMTEngine/Models/Models.py`: Defines the data models used in the application. Should be agreed with input json.  
`SMTEngine/Rules/`:
* `Compare.py`: Contains the logic for compare rules.
* `Report.py`: Contains the logic for report rules.

`SMTEngine/utils/`:
* `compare_utils.py`: Utility functions to support compare rules.
* `report_utils.py`: Utility functions to support report rules.

`SMTEngine/API.py`: Defines the FastAPI application and endpoints.

## Project Metadata
`.gitignore`: Specifies files and directories to be ignored by Git.  
`Dockerfile`: Instructions to build a Docker image for the project.  
`MANIFEST.in`: Specifies additional files to include in the package distribution.  
`requirements.txt`: Lists the Python dependencies required by the project.  
`setup.py`: Setup script for packaging and distributing the project.  


# Getting Started
## Prerequisites
* Python 3.8 or higher  
* Docker (optional, for containerization)

## Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/my_fastapi_project.git
cd my_fastapi_project
```
2. Install the dependencies:
```
pip install -r requirements.txt
```
3. Set up the configuration:  
*Update the `config/key_config.yaml` file with your configuration settings.*

## Running the Application
### 1. Using Python
#### Run the FastAPI application:
```
uvicorn SMTEngine.API:app --reload
```
### 2. Using Docker
#### Build the Docker image:
```
docker build -t smtengine .
```
#### Run the Docker container:
```
docker run -p 8000:8000 --mount type=bind,source="PATH/TO/DATASETS",target=/app/data smtengine
```
> NOTE: Replace "PATH/TO/DATASETS" with the actual path where datasets are kept. This path should be sent in request as well