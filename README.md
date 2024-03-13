## Wobot App

### 1. Clone the repository

```bash
git clone https://github.com/atharvabhide/Wobot-App.git
cd Wobot-App
```

### 2. Install Docker and Docker Compose

[Install Docker](https://docs.docker.com/engine/install/)

[Install Docker Compose](https://docs.docker.com/compose/install/)

### 3. Build and Run the Docker Container with bash

```bash
./run.sh start-dev
```

### 4. Navigate to the following URL for the API documentation (Swagger/Redoc)

```bash
http://localhost:8080/docs/
http://localhost:8080/redoc/
```

### 5. Before pushing, run the check-syntax command and rectify the errors

```bash
./run.sh check-syntax
```

### 6. To stop the application, run the following command
```bash
./run.sh stop-dev
```

### 7. If running locally, then create the .env file and add the environment variables
```bash
touch .env
```

### 8. Install the required packages using the following command
```bash
pip install -r requirements.txt
```

### 9. Then start the application using the following command
```bash
python app/main.py
```