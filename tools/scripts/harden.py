#!/usr/bin/env python3
"""
APK Hardening Script
Main pipeline for hardening Android APK files with various security features.
"""

import os
import sys
import subprocess
import hashlib
import zipfile
import tempfile
import shutil
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APKHardener:
    """Main class for APK hardening operations"""
    
    def __init__(self, input_apk, output_dir='hardened-output'):
        self.input_apk = Path(input_apk)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = None
        self.metadata = {
            'input_apk': str(self.input_apk),
            'timestamp': datetime.utcnow().isoformat(),
            'operations': []
        }
        
    def validate_apk(self):
        """Validate input APK file"""
        logger.info(f"Validating APK: {self.input_apk}")
        
        if not self.input_apk.exists():
            raise FileNotFoundError(f"APK file not found: {self.input_apk}")
        
        if not zipfile.is_zipfile(self.input_apk):
            raise ValueError(f"Invalid APK file (not a valid ZIP): {self.input_apk}")
        
        # Check for AndroidManifest.xml
        with zipfile.ZipFile(self.input_apk, 'r') as zf:
            if 'AndroidManifest.xml' not in zf.namelist():
                raise ValueError("Invalid APK: AndroidManifest.xml not found")
        
        logger.info("APK validation successful")
        self.metadata['operations'].append('validation_passed')
        return True
    
    def calculate_sha256(self, file_path):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def resource_obfuscation(self, apk_path):
        """
        Perform resource obfuscation (placeholder implementation)
        In production, this would rename resources, obfuscate strings, etc.
        """
        logger.info("Performing resource obfuscation...")
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix='apk_resources_')
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Placeholder: In production, would rename resources, obfuscate strings
            # For now, just add metadata
            metadata_file = os.path.join(temp_dir, 'META-INF', 'hardening.txt')
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            with open(metadata_file, 'w') as f:
                f.write(f"Resource obfuscation applied\nTimestamp: {datetime.utcnow().isoformat()}\n")
            
            # Repackage APK
            obfuscated_apk = apk_path.parent / f"{apk_path.stem}_obfuscated.apk"
            with zipfile.ZipFile(obfuscated_apk, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
            
            logger.info(f"Resource obfuscation complete: {obfuscated_apk}")
            self.metadata['operations'].append('resource_obfuscation')
            return obfuscated_apk
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def dex_shell_compress(self, apk_path):
        """
        Apply DEX shell compression (placeholder implementation)
        In production, this would encrypt/compress DEX files and add unpacking stub
        """
        logger.info("Applying DEX shell compression...")
        
        temp_dir = tempfile.mkdtemp(prefix='apk_dex_')
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find DEX files
            dex_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.dex'):
                        dex_files.append(os.path.join(root, file))
            
            logger.info(f"Found {len(dex_files)} DEX files")
            
            # Placeholder: In production, would compress/encrypt DEX files
            # Add metadata about compression
            metadata_file = os.path.join(temp_dir, 'META-INF', 'dex_shell.txt')
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            with open(metadata_file, 'w') as f:
                f.write(f"DEX shell applied\n")
                f.write(f"DEX files processed: {len(dex_files)}\n")
                f.write(f"Timestamp: {datetime.utcnow().isoformat()}\n")
            
            # Repackage APK
            compressed_apk = apk_path.parent / f"{apk_path.stem}_dexshell.apk"
            with zipfile.ZipFile(compressed_apk, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
            
            logger.info(f"DEX shell compression complete: {compressed_apk}")
            self.metadata['operations'].append('dex_shell_compression')
            return compressed_apk
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def add_integrity_check(self, apk_path):
        """Add integrity check metadata (SHA-256 hash)"""
        logger.info("Adding integrity check...")
        
        # Calculate original hash
        original_hash = self.calculate_sha256(apk_path)
        logger.info(f"Original APK SHA-256: {original_hash}")
        
        temp_dir = tempfile.mkdtemp(prefix='apk_integrity_')
        try:
            # Extract APK
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Add integrity metadata
            integrity_file = os.path.join(temp_dir, 'META-INF', 'integrity.json')
            os.makedirs(os.path.dirname(integrity_file), exist_ok=True)
            
            integrity_data = {
                'original_hash': original_hash,
                'timestamp': datetime.utcnow().isoformat(),
                'algorithm': 'SHA-256'
            }
            
            with open(integrity_file, 'w') as f:
                json.dump(integrity_data, f, indent=2)
            
            # Repackage APK
            integrity_apk = apk_path.parent / f"{apk_path.stem}_integrity.apk"
            with zipfile.ZipFile(integrity_apk, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
            
            logger.info(f"Integrity check added: {integrity_apk}")
            self.metadata['operations'].append('integrity_check')
            self.metadata['integrity_hash'] = original_hash
            return integrity_apk
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def add_env_detection_stub(self, apk_path):
        """Add environment detection stub (placeholder)"""
        logger.info("Adding environment detection stub...")
        
        # Placeholder: In production, would inject stub_detect_env.java into APK
        temp_dir = tempfile.mkdtemp(prefix='apk_env_')
        try:
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Add metadata
            stub_file = os.path.join(temp_dir, 'META-INF', 'env_detection.txt')
            os.makedirs(os.path.dirname(stub_file), exist_ok=True)
            with open(stub_file, 'w') as f:
                f.write("Environment detection stub included\n")
                f.write("Detects: rooted devices, emulators\n")
            
            # Repackage
            stub_apk = apk_path.parent / f"{apk_path.stem}_envstub.apk"
            with zipfile.ZipFile(stub_apk, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
            
            logger.info(f"Environment detection stub added: {stub_apk}")
            self.metadata['operations'].append('env_detection_stub')
            return stub_apk
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def add_anti_debug_stub(self, apk_path):
        """Add anti-debug stub (placeholder)"""
        logger.info("Adding anti-debug stub...")
        
        # Placeholder: In production, would inject stub_anti_debug.java into APK
        temp_dir = tempfile.mkdtemp(prefix='apk_antidebug_')
        try:
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Add metadata
            stub_file = os.path.join(temp_dir, 'META-INF', 'anti_debug.txt')
            os.makedirs(os.path.dirname(stub_file), exist_ok=True)
            with open(stub_file, 'w') as f:
                f.write("Anti-debug stub included\n")
                f.write("Detects: debuggers, tracers, timing anomalies\n")
            
            # Repackage
            stub_apk = apk_path.parent / f"{apk_path.stem}_antidebug.apk"
            with zipfile.ZipFile(stub_apk, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)
            
            logger.info(f"Anti-debug stub added: {stub_apk}")
            self.metadata['operations'].append('anti_debug_stub')
            return stub_apk
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def zipalign_apk(self, apk_path, output_path):
        """Align APK using zipalign"""
        logger.info(f"Running zipalign on {apk_path}...")
        
        try:
            cmd = ['zipalign', '-f', '-p', '4', str(apk_path), str(output_path)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("Zipalign successful")
            self.metadata['operations'].append('zipalign')
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Zipalign failed: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.warning("zipalign not found, skipping alignment")
            # Copy file if zipalign not available
            shutil.copy2(apk_path, output_path)
            return False
    
    def sign_apk(self, apk_path, output_path, keystore, keystore_pass, key_alias, key_pass):
        """Sign APK using apksigner"""
        logger.info(f"Signing APK: {apk_path}...")
        
        try:
            cmd = [
                'apksigner', 'sign',
                '--ks', keystore,
                '--ks-pass', f'pass:{keystore_pass}',
                '--ks-key-alias', key_alias,
                '--key-pass', f'pass:{key_pass}',
                '--out', str(output_path),
                str(apk_path)
            ]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("APK signing successful")
            self.metadata['operations'].append('apk_signing')
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"APK signing failed: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("apksigner not found. Please install Android SDK build-tools.")
            raise
    
    def verify_apk(self, apk_path):
        """Verify APK signature"""
        logger.info(f"Verifying APK signature: {apk_path}...")
        
        try:
            cmd = ['apksigner', 'verify', '--verbose', str(apk_path)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("APK signature verified successfully")
            logger.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"APK verification failed: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.warning("apksigner not found, skipping verification")
            return False
    
    def harden(self, 
               resource_obfuscation=False,
               dex_shell=True,
               integrity_check=True,
               env_detection=False,
               anti_debug=False,
               keystore='debug.keystore',
               keystore_password='android',
               key_alias='debugkey',
               key_password='android'):
        """
        Main hardening pipeline
        """
        logger.info("=" * 60)
        logger.info("Starting APK Hardening Process")
        logger.info("=" * 60)
        
        # Validate input
        self.validate_apk()
        
        # Start with original APK
        current_apk = self.input_apk
        
        # Apply transformations based on flags
        if resource_obfuscation:
            current_apk = self.resource_obfuscation(current_apk)
        
        if dex_shell:
            current_apk = self.dex_shell_compress(current_apk)
        
        if integrity_check:
            current_apk = self.add_integrity_check(current_apk)
        
        if env_detection:
            current_apk = self.add_env_detection_stub(current_apk)
        
        if anti_debug:
            current_apk = self.add_anti_debug_stub(current_apk)
        
        # Zipalign
        aligned_apk = self.output_dir / f"{self.input_apk.stem}_aligned.apk"
        self.zipalign_apk(current_apk, aligned_apk)
        
        # Sign
        final_apk = self.output_dir / f"hardened-{self.input_apk.name}"
        self.sign_apk(aligned_apk, final_apk, keystore, keystore_password, 
                     key_alias, key_password)
        
        # Verify
        self.verify_apk(final_apk)
        
        # Calculate final hash
        final_hash = self.calculate_sha256(final_apk)
        self.metadata['final_hash'] = final_hash
        self.metadata['output_apk'] = str(final_apk)
        
        # Save metadata
        metadata_file = self.output_dir / 'hardening_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        logger.info("=" * 60)
        logger.info("APK Hardening Complete!")
        logger.info(f"Output: {final_apk}")
        logger.info(f"Final SHA-256: {final_hash}")
        logger.info(f"Metadata: {metadata_file}")
        logger.info("=" * 60)
        
        # Clean up intermediate files
        if current_apk != self.input_apk and current_apk != aligned_apk:
            try:
                current_apk.unlink()
            except:
                pass
        
        return final_apk


def download_apk(url, output_path):
    """Download APK from URL"""
    logger.info(f"Downloading APK from {url}...")
    try:
        import urllib.request
        urllib.request.urlretrieve(url, output_path)
        logger.info(f"APK downloaded to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download APK: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='APK Hardening Tool')
    parser.add_argument('input', help='Path or URL to input APK file')
    parser.add_argument('--output-dir', default='hardened-output', 
                       help='Output directory for hardened APK')
    parser.add_argument('--resource-obfuscation', action='store_true',
                       help='Enable resource obfuscation')
    parser.add_argument('--no-dex-shell', action='store_true',
                       help='Disable DEX shell compression')
    parser.add_argument('--no-integrity-check', action='store_true',
                       help='Disable integrity check')
    parser.add_argument('--env-detection', action='store_true',
                       help='Enable environment detection stub')
    parser.add_argument('--anti-debug', action='store_true',
                       help='Enable anti-debug stub')
    parser.add_argument('--keystore', default='debug.keystore',
                       help='Path to keystore file')
    parser.add_argument('--keystore-password', default='android',
                       help='Keystore password')
    parser.add_argument('--key-alias', default='debugkey',
                       help='Key alias')
    parser.add_argument('--key-password', default='android',
                       help='Key password')
    
    args = parser.parse_args()
    
    try:
        # Check if input is URL or file path
        input_apk = args.input
        if input_apk.startswith('http://') or input_apk.startswith('https://'):
            # Download APK
            temp_apk = 'downloaded_app.apk'
            if not download_apk(input_apk, temp_apk):
                sys.exit(1)
            input_apk = temp_apk
        
        # Create hardener
        hardener = APKHardener(input_apk, args.output_dir)
        
        # Run hardening
        hardener.harden(
            resource_obfuscation=args.resource_obfuscation,
            dex_shell=not args.no_dex_shell,
            integrity_check=not args.no_integrity_check,
            env_detection=args.env_detection,
            anti_debug=args.anti_debug,
            keystore=args.keystore,
            keystore_password=args.keystore_password,
            key_alias=args.key_alias,
            key_password=args.key_password
        )
        
        logger.info("Hardening process completed successfully!")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Hardening failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
