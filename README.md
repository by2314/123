# 123 - APK Hardening Framework

这是一个仓库 / This is a repository

## Overview

This repository provides an APK hardening framework with a GitHub Actions workflow to automatically build and harden Android APK files with various security features.

## Features

The APK hardening framework supports:

- **Resource Obfuscation**: Obfuscate resources and strings (placeholder implementation)
- **DEX Shell Compression**: Compress/encrypt DEX files (placeholder implementation)
- **Integrity Check**: Add SHA-256 hash metadata for integrity verification
- **Environment Detection**: Add stubs to detect rooted devices and emulators
- **Anti-Debug Detection**: Add stubs to detect debugging attempts
- **APK Signing**: Sign hardened APKs with your keystore or auto-generated debug keystore
- **APK Alignment**: Optimize APK with zipalign

## Quick Start

### Using GitHub Actions Workflow

1. **Navigate to Actions tab** in your repository
2. **Select "APK Hardening Workflow"**
3. **Click "Run workflow"**
4. **Configure inputs:**
   - `apk_source`: Path (e.g., `input/app.apk`) or URL to your APK
   - Toggle hardening features as needed
5. **Run the workflow**
6. **Download artifacts** (hardened APK and logs) after completion

### Using Command Line

```bash
# Basic usage with defaults (DEX shell + integrity check enabled)
python3 tools/scripts/harden.py input/app.apk

# With all features enabled
python3 tools/scripts/harden.py input/app.apk \
  --resource-obfuscation \
  --env-detection \
  --anti-debug

# With custom keystore
python3 tools/scripts/harden.py input/app.apk \
  --keystore my.keystore \
  --keystore-password mypass \
  --key-alias myalias \
  --key-password keypass

# From URL
python3 tools/scripts/harden.py https://example.com/app.apk
```

## Workflow Configuration

### Inputs

The workflow accepts the following inputs:

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `apk_source` | string | `input/app.apk` | Path or URL to source APK |
| `resource_obfuscation` | boolean | `false` | Enable resource obfuscation |
| `dex_shell` | boolean | `true` | Enable DEX shell compression |
| `integrity_check` | boolean | `true` | Enable integrity check |
| `env_detection` | boolean | `false` | Enable environment/root detection |
| `anti_debug` | boolean | `false` | Enable anti-debug detection |

### Secrets (Optional)

Configure these secrets in your repository settings for production signing:

| Secret | Description |
|--------|-------------|
| `KEYSTORE_BASE64` | Base64-encoded keystore file |
| `KEYSTORE_PASSWORD` | Keystore password |
| `KEY_ALIAS` | Key alias in keystore |
| `KEY_PASSWORD` | Key password |

**If secrets are not configured**, the workflow automatically generates a debug keystore.

#### Creating Base64-encoded Keystore

```bash
base64 -i your.keystore | pbcopy  # macOS
base64 -i your.keystore | xclip   # Linux
```

### Outputs

The workflow produces the following artifacts:

- **hardened-apk**: Contains the hardened APK file (`hardened-*.apk`) and metadata
- **hardening-logs**: Contains detailed logs and metadata JSON

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── harden.yml          # GitHub Actions workflow
├── tools/
│   ├── config/
│   │   └── proguard-rules.pro  # ProGuard/R8 rules template
│   └── scripts/
│       ├── harden.py           # Main hardening script
│       ├── prepare_keystore.sh # Keystore preparation
│       ├── stub_detect_env.java     # Environment detection stub
│       └── stub_anti_debug.java     # Anti-debug detection stub
├── input/                      # Place APKs here for local processing
│   └── README.md
├── .gitignore
└── README.md
```

## Requirements

### For GitHub Actions

- No manual setup required - all dependencies installed automatically

### For Local Usage

- Python 3.7+
- Android SDK Build Tools (zipalign, apksigner)
- Java Development Kit (JDK) 8+

#### Installing Android SDK Build Tools

**macOS:**
```bash
brew install android-platform-tools
brew install --cask android-commandlinetools
```

**Ubuntu/Debian:**
```bash
sudo apt-get install android-sdk-platform-tools
# Or download from https://developer.android.com/studio/releases/platform-tools
```

**Manual Installation:**
1. Download Android SDK Platform Tools from [Android Developer site](https://developer.android.com/studio/releases/platform-tools)
2. Extract and add to PATH
3. Install build-tools: `sdkmanager "build-tools;34.0.0"`

## Script Usage

### harden.py

Main APK hardening script.

```bash
usage: harden.py [-h] [--output-dir OUTPUT_DIR] [--resource-obfuscation]
                 [--no-dex-shell] [--no-integrity-check] [--env-detection]
                 [--anti-debug] [--keystore KEYSTORE]
                 [--keystore-password KEYSTORE_PASSWORD] [--key-alias KEY_ALIAS]
                 [--key-password KEY_PASSWORD]
                 input

positional arguments:
  input                 Path or URL to input APK file

optional arguments:
  --output-dir OUTPUT_DIR       Output directory (default: hardened-output)
  --resource-obfuscation        Enable resource obfuscation
  --no-dex-shell               Disable DEX shell compression
  --no-integrity-check         Disable integrity check
  --env-detection              Enable environment detection stub
  --anti-debug                 Enable anti-debug stub
  --keystore KEYSTORE          Path to keystore file (default: debug.keystore)
  --keystore-password PASSWORD Keystore password (default: android)
  --key-alias ALIAS            Key alias (default: debugkey)
  --key-password PASSWORD      Key password (default: android)
```

### prepare_keystore.sh

Keystore preparation script.

```bash
./tools/scripts/prepare_keystore.sh [keystore_path] [keystore_password] [key_alias] [key_password]

# Uses KEYSTORE_BASE64 environment variable if set, otherwise generates debug keystore
```

## Development

### Linting Scripts

```bash
# Python linting
python3 -m py_compile tools/scripts/harden.py

# Bash linting (requires shellcheck)
shellcheck tools/scripts/prepare_keystore.sh
```

### Testing Locally

1. Place a test APK in `input/` directory
2. Run the hardening script:
   ```bash
   python3 tools/scripts/harden.py input/test.apk
   ```
3. Check output in `hardened-output/` directory

## Security Considerations

⚠️ **Important Notes:**

1. **Debug Keystore**: The auto-generated debug keystore is for testing only. For production, always use your own keystore via secrets.

2. **Placeholder Implementations**: Some features (resource obfuscation, DEX shell) are placeholder implementations. They add metadata but don't perform full obfuscation/encryption. Extend these for production use.

3. **Secrets Management**: Never commit keystores or passwords to the repository. Use GitHub Secrets or environment variables.

4. **APK Validation**: Always validate hardened APKs before distribution.

## Troubleshooting

### "zipalign not found" or "apksigner not found"

Install Android SDK Build Tools:
```bash
# See Requirements section above
```

### "APK signing failed"

- Check keystore path and credentials
- Ensure keystore is valid: `keytool -list -keystore your.keystore`

### Workflow fails with keystore error

- Verify secrets are correctly set in repository settings
- Check base64 encoding is correct
- Ensure keystore passwords match

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and development purposes.

## Acknowledgments

- Android SDK Build Tools
- ProGuard/R8 for obfuscation capabilities
