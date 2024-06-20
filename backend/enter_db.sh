# Execute Docker Compose command to enter the Docker container and run psql
docker-compose exec db bash -c "psql -U postgres -d app"
