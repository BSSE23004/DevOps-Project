# DevOps-Project

# Local dev

docker-compose build
docker-compose up -d
docker-compose logs -f

# List containers/images

docker ps
docker images

# Stop / remove

docker-compose down

# Tag & push

docker tag study-api:local YOUR_DOCKERHUB_USERNAME/study-api:latest
docker push YOUR_DOCKERHUB_USERNAME/study-api:latest

# Kubernetes

kubectl apply -f kubernetes/
kubectl get pods -o wide
kubectl get svc
kubectl port-forward svc/frontend-service 8080:80

# Rolling update

kubectl set image deployment/frontend-deployment frontend=YOUR_DOCKERHUB_USERNAME/study-frontend:latest
kubectl rollout status deployment/frontend-deployment
