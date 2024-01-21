# Blockchain Donation App

Welcome to the Blockchain Donation App repository! This repository contains the code for the backend FastAPI application and the frontend Vue.js app.

## Running UNICEF Test API

The test API is built on the FastAPI Python 3 framework and runs on the Windows Subsystem for Linux (WSL2) Ubuntu 22 LTS environment. Follow the instructions below to set up the API:

1. **Create a Python 3 Virtual Environment:**

   ```bash
   python3 -m venv unicef_api_env
   ```

2. **Start the environment**

   ```bash
   source unicef_api_env/bin/activate
   ```

3. **In the app api directory**

   ```bash
   mkdir unicef_api
   ```

4. **Install the fastapi all dependecies using , extract and navigate to the unice_api folder**

   ````bash
   cd  unicef_api
    ```
    ```bash
   pip3 install -r requirements. txt
   ````

5. **Create the .env file**

   ```bash
   DATABASE_PORT=6500
   MYSQL_PASSWORD=db_password
   MYSQL_USER=db_user
   MYSQL_DB=db_name
   MYSQL_HOST=mysql
   MYSQL_HOSTNAME=localhost
   ```

   ```bash
   CLIENT_ORIGIN=http://localhost:8080
   BASE_URL=http://localhost:8000
   ```

   ```bash
   ACCESS_TOKEN_EXPIRES_IN=20
   REFRESH_TOKEN_EXPIRES_IN=60000
   ```

   ```bash
   SECRET_KEY = LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FESytmYXluRERVeWIwMWZXNkp2RURPM3VBZgp3bzJPMTdrRHppZERIOUNSdVZ6WVppK2NNSTFqYzZKYmxKdTBOWHk0N1NudlpJS2tOaW1ONzRyQ1RhUEpXWDR4CmZibmROZ2V3MGZYRC9aSUpBM2RENHVLem1pdnVMd0ZtcHZydGFxNVZyTjltcmRvQ3NUU1RiN1JBbWlsSkZVUWQKSWt3NTc5VDRzckJsdjBTL2p3SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ
   ALGORITHM = HS256
   ```

6. **Start the api**

```bash
$uvicorn main:app --reload
```

## Running UNICEF Test Frontend

The frontend is a vue app, to run the app first install all the node modules by running the commands below:

1. **Extract the unicef_fe content and navigate to the folder**

   ```bash
   $cd unicef_fe
   ```

2. **Install modules**

   ```bash
   npm install
   ```

3. **Run the app**
   ```bash
   npm run dev
   ```

Note: Ensure you have Node.js and npm installed on your machine.
