#!/usr/bin/env python3
"""
concat_potcar.py  (always treats last argument as output file name)

Usage:
    python concat_potcar.py POTCAR_P POTCAR_Mn POTCAR_H POTCAR_PMnH
"""

import sys
from pathlib import Path

def get_symbol(potcar_path: Path) -> str:
    """Extract the element symbol from the first non-empty line."""
    with potcar_path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]
                else:
                    raise ValueError(f"Cannot parse symbol: {line}")
    raise ValueError(f"POTCAR {potcar_path} is empty")

def main():
    if len(sys.argv) < 3:
        print("Error: Need at least two input POTCARs and one output name.")
        print(__doc__)
        sys.exit(1)

    *potcar_args, out_name = sys.argv[1:]
    potcar_files = [Path(p) for p in potcar_args]
    out_path = Path(out_name)

    # Verify input files exist
    for p in potcar_files:
        if not p.is_file():
            print(f"Error: File not found: {p}")
            sys.exit(1)

    # Concatenate without extra newlines
    with out_path.open('w', encoding='utf-8') as outfile:
        for p in potcar_files:
            with p.open('r', encoding='utf-8') as infile:
                outfile.write(infile.read())

    symbols = [get_symbol(p) for p in potcar_files]
    print(f"✅ Success: Created {out_path} ({len(potcar_files)} sections, order: {' → '.join(symbols)})")

if __name__ == "__main__":
    main()
