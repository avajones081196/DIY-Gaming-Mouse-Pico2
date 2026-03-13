"""
assembly_original.py  —  DIY Gaming Mouse Pico 2
==================================================
Assembles the 6 ORIGINAL source STL files into assembly_original.stl
Used as reference for comparison against assembly.stl
"""
import os, struct
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

def stl_volume(path):
    """Calculate volume directly from STL triangles using divergence theorem."""
    with open(path, 'rb') as f:
        f.read(80)
        count = struct.unpack('<I', f.read(4))[0]
        vol = 0.0
        for _ in range(count):
            f.read(12)
            v = [struct.unpack('<3f', f.read(12)) for _ in range(3)]
            f.read(2)
            vol += (v[0][0]*(v[1][1]*v[2][2]-v[1][2]*v[2][1])
                  - v[0][1]*(v[1][0]*v[2][2]-v[1][2]*v[2][0])
                  + v[0][2]*(v[1][0]*v[2][1]-v[1][1]*v[2][0])) / 6.0
    return abs(vol)

PARTS = [
    ("mouse shell progress pico 2 bottom.stl",      "bottom"),
    ("mouse shell progress pico 2 top.stl",         "top"),
    ("mouse shell progress pico 2 thumb a.stl",     "thumb_a"),
    ("mouse shell progress pico 2 thumb b.stl",     "thumb_b"),
    ("mouse shell progress pico 2 wheel.stl",       "wheel"),
    ("mouse shell progress pico 2 wheel brace.stl", "wheel_brace"),
]

loaded_parts = []
loaded_names = []
missing = []

print("Loading ORIGINAL source STLs...")
for filename, label in PARTS:
    path = os.path.join(_HERE, filename)
    if os.path.exists(path):
        part = import_stl(path)
        vol = stl_volume(path)
        loaded_parts.append(part)
        loaded_names.append(label)
        print(f"  ✓ {label:15s}  {vol:10.3f} mm³")
    else:
        missing.append(filename)
        print(f"  ✗ {label:15s}  NOT FOUND — check filename: {filename}")

if missing:
    print(f"\n⚠️  Missing {len(missing)} file(s): {', '.join(missing)}")

if loaded_parts:
    total = sum(stl_volume(os.path.join(_HERE, f)) for f, _ in PARTS
                if os.path.exists(os.path.join(_HERE, f)))
    print(f"\n  {'TOTAL':15s}  {total:10.3f} mm³")

    show(*loaded_parts, names=loaded_names)

    print(f"\nExporting original assembly STL...")
    assembly_orig = Compound(loaded_parts)
    out_path = os.path.join(_HERE, "assembly_original.stl")
    export_stl(assembly_orig, out_path)
    print(f"  ✓ Exported: {out_path}")
    print(f"  ✓ Total volume: {total:.3f} mm³")
else:
    print("\nNo parts loaded.")
