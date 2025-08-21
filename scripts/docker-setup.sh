#!/bin/bash

# Docker setup script for BE-Events project

set -e

echo "🚀 Setting up Docker environment for BE-Events..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database Configuration
POSTGRES_DB=events_db
POSTGRES_USER=events_user
POSTGRES_PASSWORD=events_password

# Application Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Environment
ENVIRONMENT=development
EOF
    echo "✅ .env file created"
else
    echo "ℹ️  .env file already exists"
fi

# Generate SSL certificates for development
echo "🔐 Generating SSL certificates..."
chmod +x scripts/generate-ssl.sh
./scripts/generate-ssl.sh

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis

# Set proper permissions
echo "🔒 Setting proper permissions..."
chmod 755 scripts/
chmod 644 .env

echo "✅ Docker setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review and modify .env file if needed"
echo "2. Run 'docker-compose -f docker-compose.dev.yml up --build' for development"
echo "3. Run 'docker-compose up --build' for production"
echo "4. Run 'docker-compose -f docker-compose.test.yml up --build' for testing"
echo ""
echo "🌐 Access points:"
echo "- Application: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/docs"
echo "- Database: localhost:5432"
echo "- Redis: localhost:6379"
