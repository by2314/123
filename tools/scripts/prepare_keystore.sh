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
    
    # Create temporary password files for secure password passing
    TEMP_STORE_PASS=$(mktemp)
    TEMP_KEY_PASS=$(mktemp)
    echo "$KEYSTORE_PASSWORD" > "$TEMP_STORE_PASS"
    echo "$KEY_PASSWORD" > "$TEMP_KEY_PASS"
    
    # Generate a debug keystore using keytool with password files
    keytool -genkeypair \
        -keystore "$KEYSTORE_PATH" \
        -alias "$KEY_ALIAS" \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -storepass:file "$TEMP_STORE_PASS" \
        -keypass:file "$TEMP_KEY_PASS" \
        -dname "CN=Debug, OU=Debug, O=Debug, L=Debug, ST=Debug, C=US" \
        -noprompt
    
    # Clean up temp files
    rm -f "$TEMP_STORE_PASS" "$TEMP_KEY_PASS"
    
    echo "Debug keystore generated successfully at $KEYSTORE_PATH"
fi

# Verify keystore exists and is readable
if [ ! -f "$KEYSTORE_PATH" ]; then
    echo "ERROR: Keystore file not found at $KEYSTORE_PATH"
    exit 1
fi

echo "Keystore prepared successfully"
echo "Keystore info:"
# Create temp password file for listing
TEMP_PASS=$(mktemp)
echo "$KEYSTORE_PASSWORD" > "$TEMP_PASS"
keytool -list -keystore "$KEYSTORE_PATH" -storepass:file "$TEMP_PASS" || true
rm -f "$TEMP_PASS"

exit 0
