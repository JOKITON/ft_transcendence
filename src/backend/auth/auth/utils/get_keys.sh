# Generate RSA keys if they don't exist

# Store current working directory
CURRENT_DIR=$(pwd)

# Check if the environment variable is set
if [ -z "$MIGRATION_CONTAINER" ]; then
  echo "MIGRATION_CONTAINER is not set in the environment."
  # Set KEY_DIR to include the default directory
  KEY_DIR="/auth/secrets"
else
  echo "MIGRATION_CONTAINER is set to: $MIGRATION_CONTAINER"
  # Set KEY_DIR to include the current directory
  KEY_DIR="$CURRENT_DIR/auth/secrets"
fi

# Create the directory if it doesn't exist
mkdir -p "$KEY_DIR"

AUTH_PUBLIC_KEY_PATH="$KEY_DIR/public.pem"
AUTH_PRIVATE_KEY_PATH="$KEY_DIR/private.pem"

echo "Waiting for Keys to start..."
while ! nc -z keys 80; do
  sleep 0.1
done

# Fetch public key from JWT Key Management Service
curl -o $AUTH_PUBLIC_KEY_PATH http://keys/api/v1/keys/public
if ! openssl rsa -pubin -in $AUTH_PUBLIC_KEY_PATH -text -noout >/dev/null 2>&1; then
  echo "Error: Fetched public key is not valid."
  exit 1
fi

curl -o $AUTH_PRIVATE_KEY_PATH http://keys/api/v1/keys/private
if ! openssl rsa -in $AUTH_PRIVATE_KEY_PATH -check >/dev/null 2>&1; then
  echo "Error: Fetched private key is not valid."
  exit 1
fi
