# Convert filed book to database by API

Read and store the data from filed book using Phe_API_store service [Api Store](https://github.com/carlosmorenophd/phen_api_store).

## Requirements:

### Hardware Requirements: 

The recommended computer for deploying this application should have at least a quad-core processor, 4GB of RAM, and 250GB of hard disk space for initial testing.

These requirements are specifically for the Phen_API_STORE. Additional systems will be installed on the same machine. For experimental and production use, consider upgrading to a system with an eight-core 16-thread processor, 24GB of RAM, and 2.5TB of storage, similar to our current setup.

### Operating System: 

Ubuntu `22.04` is the recommended operating system due to its up-to-date kernel and configurations that are optimized for application deployment. While Windows, macOS, or other systems can be used, they will require installing Docker in a Linux container with x86-64 architecture.

### Software Requirements: 

Docker is the only software required for this project. Please install it from the [official repository](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) to ensure compatibility and proper execution of the following commands.


## Run application


1. Install and run the data storage service:

Download and install the service from a publicly available repository [Api Store](https://github.com/carlosmorenophd/phen_api_store).

2. Rename the file `example.env` to `.env` put the variables form url from phen api store, path to folder to process:


```
URL_DATA_WAREHOUSE=url_to_service_PHEN_API_STORE
PATH_TO_CACHE=folder_to_store_zip_file_to_process
FOLDER_DATA=/app/cache/
DEBUG=TRUE
```
**Notes:**
* `DEBUG` variable enable some prompt from service
* `FOLDER_DATA` variable to mount point into container keep it `/app/cache/`
* `PATH_TO_CACHE` variable where the user can put the files to process it

3. Command to run the container

```shell
docker compose -f compose.yaml up -d
```
4. Place data files:

Put your zip files in a folder that linked by the variable `PATH_TO_CACHE` in some folder called `files`.

5. Process data:

The service every 6 seconds review this folder to process new files and store on database.

6. Analyze data:

Use a separate tool [Api Fetch](https://github.com/carlosmorenophd/phen_api_fetch) to filter the stored data and create analysis datasets.


## Get data

The data used to test and create this script was sourced from CIMMYT's Dataverse (link to CIMMYT Dataverse). Specifically, data from the IWIS project was used.


* Example files can be found in the "examples" folder.

Global Wheat Program; IWIN Collaborators; Ammar, Karim; Saint Pierre, Carolina, 2023, "54th International Durum Yield Nursery", https://hdl.handle.net/11529/10548803, CIMMYT Research Data & Software Repository Network, V2



## About author


In collaboration with the [Universidad Autonoma del Estado de Mexico](https://www.uaemex.mx/), supported by [CONAHCYT](https://conahcyt.mx/) scholarships and supported by [CIMMYT](https://www.cimmyt.org/es/), this project was created. For new features, changes, or improvements, please reach out to:

Student, Ph.D. Juan Carlos Moreno Sanchez

* **[Scholar email](mailto:jcmorenos001@alumno.uaemex.mx)**
* **[Personal email](mailto:carlos.moreno.phd@gmail.com)**


