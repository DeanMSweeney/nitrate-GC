#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import math

# Check for command-line arguments
if len(sys.argv) == 1:
    print("Usage: dosanalyze.py [w=number widths at quarter-height to include] [e=emin,emax] <s,p,d,a (all)> <atom num(s)>")
    sys.exit(1)

# Parse input arguments
arg1 = sys.argv[1]
e_range = bool(re.search(r'e=[-+]?\d+', arg1))  # check if energy range is specified
w = bool(re.search(r'w=\d+', arg1))  # check if width is specified
Emin = Emax = 0

# Energy range specified explicitly
if e_range:
    match = re.search(r'e=([-+]?\d+),([-+]?\d+)', arg1)
    if match:
        Emin = float(match.group(1))
        Emax = float(match.group(2))
        print(f"Integrate from {Emin} eV to {Emax} eV.")

# Check for width specification
NumStdDevs = None
if w:
    match = re.search(r'w=(\d+)', arg1)
    if match:
        NumStdDevs = int(match.group(1))
        print(f"Width: {NumStdDevs} std. devs.")

# Check if atom-specific analysis is required
atom_flag = 'd'
if len(sys.argv) > 2:
    atom_flag = sys.argv[2]
    if atom_flag not in ('s', 'p', 'd', 'a'):
        print("Error in usage syntax!")
        sys.exit(1)

# Default to analyzing all atoms (DOS0) if no atom number is given
DOSfile = "DOS0"
if len(sys.argv) > 3:
    DOSfile = "DOS1"

# Read and process the DOS file
def read_dos(file_name, cols, oflag):
    energy = []
    dos = []
    max_dos = 0
    max_dos_index = 0
    with open(file_name, 'r') as file:
        next(file)  # Skip first line
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                continue
            data = line.split()
            ene = float(data[0])
            if cols == 3:
                dos_val = float(data[1])
            elif cols == 5:
                dos_val = float(data[1]) - float(data[2])
            energy.append(ene)
            dos.append(dos_val)
            if dos_val > max_dos:
                max_dos = dos_val
                max_dos_index = len(dos) - 1
    return energy, dos, max_dos, max_dos_index

# Determine the number of columns and read the file
with open(DOSfile, 'r') as f:
    line = f.readline().strip()
    cols = len(line.split())
    print(f"Found {cols} columns in {DOSfile}")

# Read DOS data
energy, dos, max_dos, max_dos_index = read_dos(DOSfile, cols, atom_flag)

# Compute total DOS and other statistics
total_dos = sum(dos)
avg_energy = sum(ene * dos_val for ene, dos_val in zip(energy, dos)) / total_dos
energy_sq_sum = sum(ene ** 2 * dos_val for ene, dos_val in zip(energy, dos))
energy_var = energy_sq_sum / total_dos - avg_energy ** 2
energy_std = math.sqrt(energy_var)

# Width at quarter-height (if specified)
if w:
    # Calculate half-width at half-height and the corresponding indices
    cut = 0.25 * max_dos
    DOS50up = max_dos_index
    DOS50down = max_dos_index
    while dos[DOS50up] >= cut:
        DOS50up += 1
    while dos[DOS50down] >= cut:
        DOS50down -= 1
    WHH = abs(energy[DOS50up] - energy[DOS50down])
    range_width = WHH * NumStdDevs
    half_range = range_width / 2
    EneUp = energy[max_dos_index] + half_range
    EneDown = energy[max_dos_index] - half_range
    # Determine new energy range to analyze
    numenemax = next(i for i, e in enumerate(energy) if e > EneUp)
    numenemin = next(i for i in range(len(energy) - 1, -1, -1) if energy[i] < EneDown)

    print(f"Width at quarter-height: {WHH}")
    print(f"Lower energy cutoff: {energy[numenemin]}")
    print(f"Upper energy cutoff: {energy[numenemax]}")

# If no energy range is specified, use the full range
if not e_range:
    Emin = energy[0]
    Emax = energy[-1]

# Calculate the total sum for the range
dossum = 0
dstsum = 0
dssqsum = 0
for i, ene in enumerate(energy):
    if Emin <= ene <= Emax:
        dossum += dos[i]
        dstsum += ene * dos[i]
        dssqsum += ene ** 2 * dos[i]

# Compute average energy and standard deviation
eneavg = dstsum / dossum
enevar = dssqsum / dossum - eneavg ** 2
enestd = math.sqrt(enevar)

# Output results
print(f"\nTotal States: {dossum}")
print(f"Average Energy (band center): {eneavg}")
if w:
    print(f"Width at quarter-height: {WHH}")
print(f"Standard Deviation: {enestd}")

