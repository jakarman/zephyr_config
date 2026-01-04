#!/usr/bin/env python3
"""
Compare .config files and show differences between current and old versions.
"""

import sys
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

def read_config_file(filepath):
    """Read config file and return set of lines."""
    try:
        # Try UTF-8 first (most common)
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(line.rstrip('\n') for line in f if line.strip())
    except UnicodeDecodeError:
        try:
            # Try UTF-16 with BOM detection
            with open(filepath, 'r', encoding='utf-16-sig') as f:
                return set(line.rstrip('\n') for line in f if line.strip())
        except UnicodeDecodeError:
            # Try UTF-16 LE as fallback
            with open(filepath, 'r', encoding='utf-16-le') as f:
                return set(line.rstrip('\n') for line in f if line.strip())

def compare_configs(config_new, config_old):
    """Compare two config files and show differences."""
    added = config_new - config_old
    removed = config_old - config_new
    
    if not added and not removed:
        print("No changes found between .config and .config.old")
        return
    
    if removed:
        if HAS_COLOR:
            print(f"{Fore.YELLOW}=== REMOVED (in .config.old but not in .config) ==={Style.RESET_ALL}")
            for line in sorted(removed):
                print(f"{Fore.RED}- {line}{Style.RESET_ALL}")
        else:
            print("=== REMOVED (in .config.old but not in .config) ===")
            for line in sorted(removed):
                print(f"- {line}")
        print()
    
    if added:
        if HAS_COLOR:
            print(f"{Fore.YELLOW}=== ADDED (in .config but not in .config.old) ==={Style.RESET_ALL}")
            for line in sorted(added):
                print(f"{Fore.GREEN}+ {line}{Style.RESET_ALL}")
        else:
            print("=== ADDED (in .config but not in .config.old) ===")
            for line in sorted(added):
                print(f"+ {line}")
        print()
    
    if HAS_COLOR:
        print(f"{Fore.CYAN}Summary: {len(added)} added, {len(removed)} removed{Style.RESET_ALL}")
    else:
        print(f"Summary: {len(added)} added, {len(removed)} removed")

if __name__ == "__main__":
    config_path = Path("build/zephyr/.config")
    config_old_path = Path("build/zephyr/.config.old")
    
    if not config_path.exists():
        print(f"Error: {config_path} not found")
        sys.exit(1)
    
    if not config_old_path.exists():
        print(f"Error: {config_old_path} not found")
        sys.exit(1)
    
    print(f"Comparing {config_path} with {config_old_path}\n")
    
    config_new = read_config_file(config_path)
    config_old = read_config_file(config_old_path)
    
    compare_configs(config_new, config_old)
