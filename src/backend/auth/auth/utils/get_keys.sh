# Check if the directory for auth exists, if not, create it
if [ ! -d /auth/secrets ]; then
  echo "Creating /auth/secrets directory..."
  mkdir -p /auth/secrets
fi

echo "Generating private key..."
openssl genrsa -out /auth/secrets/private.pem 2048

echo "Generating public key..."
openssl rsa -in /auth/secrets/private.pem -pubout -out /auth/secrets/public.pem