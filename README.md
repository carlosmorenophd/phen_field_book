## Convert file book to database by API

### How to run it

1. Install and run the data storage service:

Download and install the service from a publicly available repository [Api Store](https://github.com/carlosmorenophd/phen_api_store).

2. Configure the container environment:

Use the provided example file (**.env.example*) to create a configuration file named *.env*.

3. Define a folder for data storage:

Configure a folder path `PATH_TO_CACHE=/mnt/cache/_phen/cache/file_book` to store zip files used by the service.

4. Run the data storage service:

Follow the initial setup instructions [Api Store](https://github.com/carlosmorenophd/phen_api_store) to run the downloaded service.

Put the url of [Api Store] into variable `URL_DATA_WAREHOUSE` to link service

5. Place data files:

Put your zip files in a folder named files within the configured data storage path (omitted).

6. Process data:

The service will store the data in its internal database.

7. Analyze data:

Use a separate tool [Api Fetch](https://github.com/carlosmorenophd/phen_api_fetch) to filter the stored data and create analysis datasets.


### Get data

The data used to test and create this script was sourced from CIMMYT's Dataverse (link to CIMMYT Dataverse). Specifically, data from the IWIS project was used.


* Example files can be found in the "examples" folder.

Global Wheat Program; IWIN Collaborators; Ammar, Karim; Saint Pierre, Carolina, 2023, "54th International Durum Yield Nursery", https://hdl.handle.net/11529/10548803, CIMMYT Research Data & Software Repository Network, V2



### About author


In collaboration with the [Universidad Autonoma del Estado de Mexico](https://www.uaemex.mx/)  and supported by [CONAHCYT](https://conahcyt.mx/) scholarships, this project was created. For new features, changes, or improvements, please reach out to:

Student, Ph.D.

Juan Carlos Moreno Sanchez

Please contact me at:

<carlos.moreno.phd@gmail.com>

<jcmorenos001@alumno.uaemex.mx>


