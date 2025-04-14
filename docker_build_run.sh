docker build -t preprocessing_server .
docker run -d --name preprocessing_server -p 8000:8000 preprocessing_server