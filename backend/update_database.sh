docker stop cai-db-1

docker rm cai-db-1

docker-compose down -v

docker-compose up -d

# Prompt user to enter message for Alembic revision
read -p "Enter a message for the Alembic revision: " message

# Run the Alembic revision command with the provided message
alembic revision --autogenerate -m "$message"

# Run the Alembic upgrade command
alembic upgrade head
