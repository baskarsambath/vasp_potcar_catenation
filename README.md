markdown
# concat_potcar.py

Simple script to concatenate VASP POTCAR files using your WINDOWS 10.

## Usage

bash
python concat_potcar.py POTCAR_1 POTCAR_2 POTCAR_3 > POTCAR_123

- All arguments except the **last one** are input files  
- The **last argument** is the output file name

## Example

bash
python concat_potcar.py POTCAR_P POTCAR_Mn POTCAR_O > POTCAR_PMnO

Output:
✅ Success: Concatenated 4 POTCARs (order: O → P → Mo → Co) → stdout

## Why use it?

- Checks that all input files exist  
- Shows the element order so you don’t make mistakes  
- No extra blank lines (safe for VASP)

Just put the script in your path and run. Needs Python 3.
