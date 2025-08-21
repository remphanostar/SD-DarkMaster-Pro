#!/usr/bin/env python3
"""
Test Cell 2 Storage Integration
Verifies that central storage is properly integrated with widgets-en.py
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

def test_storage_integration():
    """Test the storage integration functions"""
    
    print("="*60)
    print("Testing Cell 2 Storage Integration")
    print("="*60)
    
    # Import the integration module
    from cell2_storage_integration import (
        Cell2StorageIntegration,
        prepare_webui_launch,
        get_model_options,
        check_extension_compatibility
    )
    
    # Test 1: Check package status
    print("\n1. Checking package status...")
    integration = Cell2StorageIntegration()
    status = integration.check_package_status()
    
    for key, value in status.items():
        status_icon = "✅" if value else "❌"
        print(f"   {status_icon} {key}: {value}")
    
    # Test 2: Get model options
    print("\n2. Getting model options...")
    options = get_model_options()
    
    for category, models in options.items():
        print(f"\n   {category.upper()}:")
        for model in models[:2]:  # Show first 2 of each category
            print(f"      - {model['name']} ({model['size']})")
        if len(models) > 2:
            print(f"      ... and {len(models)-2} more")
    
    # Test 3: Check extension compatibility
    print("\n3. Testing extension compatibility...")
    
    test_extensions = [
        'adetailer',
        'sd-webui-controlnet',
        'sd-webui-reactor-Nsfw_freedom',
        'wd14-tagger'  # Should be incompatible with Forge
    ]
    
    for webui in ['Forge', 'ComfyUI']:
        print(f"\n   {webui}:")
        compat = check_extension_compatibility(webui, test_extensions)
        for ext, is_compat in compat.items():
            status_icon = "✅" if is_compat else "❌"
            print(f"      {status_icon} {ext}")
    
    # Test 4: Get storage report
    print("\n4. Getting storage report...")
    report = integration.get_storage_report()
    
    total_gb = report['total_size'] / (1024**3) if report['total_size'] > 0 else 0
    saved_gb = report['saved_space'] / (1024**3) if report['saved_space'] > 0 else 0
    
    print(f"   Total storage: {total_gb:.2f} GB")
    print(f"   Space saved: {saved_gb:.2f} GB")
    print(f"   Model counts: {report['model_counts']}")
    
    # Test 5: Simulate WebUI preparation (dry run)
    print("\n5. Testing WebUI preparation (dry run)...")
    
    # Don't actually download/extract, just check what would happen
    webui_type = 'ComfyUI'
    print(f"\n   Preparing {webui_type}...")
    
    # Check what would be done
    if not status['comfyui_extracted']:
        print(f"   Would extract: ComfyUI package")
    if not status['venv_ready']:
        print(f"   Would extract: Shared venv")
    
    print(f"   Would setup: Central storage symlinks")
    print(f"   Would verify: Essential models")
    
    print("\n" + "="*60)
    print("✅ Integration test complete!")
    print("="*60)

if __name__ == "__main__":
    test_storage_integration()