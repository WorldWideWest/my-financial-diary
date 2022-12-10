## Financial-Diary - Backend

## How to set it up?

You can run the application in multiple ways:

1. Run the application using the uvicorn web server locally, the process is straight forward especialy using vs code which will read the configuration in the `launch.json`, the name of this option is `Python: FastAPI` so you can go into the configuration and read about the options set to run the application this way.

   `Note:` Make sure before you run the code you have created the virtual environment, installed all packages from `requirements.txt` and have `Postgres` installed.

2. The second way is using `docker-compose`, before we run the command make sure you have docker.env file which will load the environment variables set in `docker-compose.debug.yaml` file, for now the variables are:

   ```txt
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=admin
   POSTGRES_DB=financial-dairy-db
   ```

   but in the future the list will expand and you can track here what variables are needed so you can update your local `docker.env` file.

   Now that we seted up the environment variables run the following command:

   ```bash
   docker-compose -f docker-compose.debug.yaml up --build
   ```

   once you have done that return to VS Code and then go into the debugger and select the option `Python: Remote Attach to FastApi` and then run the application.

   Now your local development environment is ready to start developing apis for the application.
