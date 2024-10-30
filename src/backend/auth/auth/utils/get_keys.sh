# Check if the directory for auth exists, if not, create it
if [ ! -d /auth/secrets ]; then
  echo "Creating /auth/secrets directory..."
  mkdir -p /auth/secrets
fi

# Check if the private key exists, if not, generate it
if [ ! -f /auth/secrets/private.pem ]; then
  echo "Generating private key..."
  openssl genrsa -out /auth/secrets/private.pem 2048

  # Verify if the private key was successfully created
  if [ -f /auth/secrets/private.pem ]; then
    echo "Private key generated successfully"
  else
    echo "Failed to generate private key"
    exit 1
  fi
else
  echo "Private key already exists"
fi

# Check if the public key exists, if not, generate it
if [ ! -f /auth/secrets/public.pem ]; then
  echo "Generating public key..."
  openssl rsa -in /auth/secrets/private.pem -pubout -out /auth/secrets/public.pem

  # Verify if the public key was successfully created
  if [ -f /auth/secrets/public.pem ]; then
    echo "Public key generated successfully"
  else
    echo "Failed to generate public key"
    exit 1
  fi
else
  echo "Public key already exists"
fi