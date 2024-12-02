# OpenMRS Setup Instructions

## MySQL Docker Container Setup

To set up a MySQL Docker container with a local volume for exchanging MySQL scripts, follow these steps:

1. **Pull the MySQL Docker image:**
   ```bash
   docker pull mysql:latest
   ```

2. **Create a volume for mysql, where I can locally place files**

3. **Run the MySQL Docker container:**

   #### Should this mounted volume be: /var/lib/mysql?

   ```bash
   docker run --name openmrs-mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 -v %USERPROFILE%/OneDrive/Hackathon/GenAI:/docker-entrypoint-initdb.d mysql:latest
   ```

4. **Verify that the MySQL container is running:**
   ```bash
   docker ps
   ```

## OpenMRS Test Data Setup

To download and install the OpenMRS test set of 5000 anonymized patients and their records, follow these steps:

1. **Download the OpenMRS test data:**
   - Visit the OpenMRS website and download the test data set of 5000 anonymized patients and their records.

2. **Extract the downloaded data:**
   - Extract the downloaded data to a local directory.

3. **Copy the extracted data to the MySQL Docker container:**
   ```bash
   docker cp /path/to/extracted/data openmrs-mysql:/docker-entrypoint-initdb.d
   ```

4. **Restart the MySQL Docker container to initialize the database with the test data:**
   ```bash
   docker restart openmrs-mysql
   ```

5. **Verify that the test data has been loaded:**
   - Connect to the MySQL container and check the database to ensure that the test data has been loaded successfully.
   ```bash
   docker exec -it openmrs-mysql mysql -uroot -proot
   ```
