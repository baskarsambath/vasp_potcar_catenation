#!/usr/bin/env python3
"""
concat_potcar.py  (outputs concatenated POTCAR to stdout — perfect for shell redirection with >)

Usage:
    python concat_potcar.py POTCAR_O POTCAR_P POTCAR_Mo POTCAR_Co > POTCAR_OPMoCo

The script concatenates ALL provided POTCAR files (in the order given) and writes
the result to stdout. Use the shell redirection ">" to save it to a file.
"""

import sys
from pathlib import Path


def get_symbol(potcar_path: Path) -> str:
    """
    Robust extraction of the element symbol from a real VASP POTCAR file.
    Looks for the standard "TITEL" or "VRHFIN" lines (the old method was too fragile).
    """
    with potcar_path.open('r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Most common: TITEL  = PAW_PBE Co 05Jan2001
            # or TITEL  = PAW_PBE Mo_pv 06Dec2000
            if 'TITEL' in line.upper():
                parts = line.split()
                try:
                    eq_idx = parts.index('=')
                    # After "=" we usually have "PAW_PBE" then the symbol (possibly with _sv, _pv, etc.)
                    if eq_idx + 2 < len(parts):
                        symbol = parts[eq_idx + 2]
                        # Strip any _suffix (Co_pv → Co, O_s → O, etc.)
                        if '_' in symbol:
                            symbol = symbol.split('_')[0]
                        return symbol
                    elif eq_idx + 1 < len(parts):
                        return parts[eq_idx + 1]
                except ValueError:
                    pass  # no "=" found, continue

            # Alternative header sometimes present: VRHFIN =Co:  d7s1
            if 'VRHFIN' in line.upper():
                parts = line.split('=', 1)
                if len(parts) > 1:
                    sym = parts[1].strip().split(':', 1)[0].strip()
                    return sym

    # Fallback (should almost never be reached for real POTCARs)
    raise ValueError(
        f"Could not find element symbol in {potcar_path}\n"
        f"   → Make sure this is a valid VASP POTCAR file."
    )


def main():
    if len(sys.argv) < 2:
        print("Error: Need at least one input POTCAR file.", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    potcar_args = sys.argv[1:]
    potcar_files = [Path(p) for p in potcar_args]

    # Verify input files exist
    for p in potcar_files:
        if not p.is_file():
            print(f"Error: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    # Concatenate everything directly to stdout (no extra newlines)
    for p in potcar_files:
        with p.open('r', encoding='utf-8', errors='ignore') as infile:
            sys.stdout.write(infile.read())

    # Show nice confirmation on stderr
    symbols = [get_symbol(p) for p in potcar_files]
    print(
        f"✅ Success: Concatenated {len(potcar_files)} POTCARs "
        f"(order: {' → '.join(symbols)}) → stdout",
        file=sys.stderr
    )


if __name__ == "__main__":
    main()
