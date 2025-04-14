docker build -t agentv-app-preprocessing-server . # Build the image
docker run -d --name agentv-app-preprocessing-server -p 8000:8000 agentv-app-preprocessing-server # Run the container
docker logs -f agentv-app-preprocessing-server # Watch logs