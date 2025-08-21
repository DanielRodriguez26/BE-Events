#!/bin/bash

# Script to generate self-signed SSL certificates for development

set -e

# Create SSL directory if it doesn't exist
mkdir -p nginx/ssl

# Generate private key
openssl genrsa -out nginx/ssl/key.pem 2048

# Generate certificate signing request
openssl req -new -key nginx/ssl/key.pem -out nginx/ssl/cert.csr -subj "/C=ES/ST=Madrid/L=Madrid/O=EventsApp/OU=Development/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -in nginx/ssl/cert.csr -signkey nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365

# Set proper permissions
chmod 600 nginx/ssl/key.pem
chmod 644 nginx/ssl/cert.pem

# Clean up CSR file
rm nginx/ssl/cert.csr

echo "SSL certificates generated successfully in nginx/ssl/"
echo "Certificate: nginx/ssl/cert.pem"
echo "Private key: nginx/ssl/key.pem"
