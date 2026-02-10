#!/bin/bash
# Keystore preparation script for APK signing
# Supports both secret-based keystores and auto-generated debug keystores

set -e

KEYSTORE_PATH="${1:-debug.keystore}"
KEYSTORE_PASSWORD="${2:-android}"
KEY_ALIAS="${3:-debugkey}"
KEY_PASSWORD="${4:-android}"

echo "Preparing keystore at: $KEYSTORE_PATH"

# Check if KEYSTORE_BASE64 environment variable is set
if [ -n "$KEYSTORE_BASE64" ]; then
    echo "Using keystore from secrets..."
    echo "$KEYSTORE_BASE64" | base64 -d > "$KEYSTORE_PATH"
    echo "Keystore decoded from base64 and saved to $KEYSTORE_PATH"
else
    echo "No keystore provided in secrets. Generating debug keystore..."
    
    # Generate a debug keystore using keytool
    keytool -genkeypair \
        -keystore "$KEYSTORE_PATH" \
        -alias "$KEY_ALIAS" \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -storepass "$KEYSTORE_PASSWORD" \
        -keypass "$KEY_PASSWORD" \
        -dname "CN=Debug, OU=Debug, O=Debug, L=Debug, ST=Debug, C=US" \
        -noprompt
    
    echo "Debug keystore generated successfully at $KEYSTORE_PATH"
fi

# Verify keystore exists and is readable
if [ ! -f "$KEYSTORE_PATH" ]; then
    echo "ERROR: Keystore file not found at $KEYSTORE_PATH"
    exit 1
fi

echo "Keystore prepared successfully"
echo "Keystore info:"
keytool -list -keystore "$KEYSTORE_PATH" -storepass "$KEYSTORE_PASSWORD" || true

exit 0
