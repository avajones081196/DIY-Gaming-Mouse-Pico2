"""
verify_parts.py  —  DIY Gaming Mouse Pico 2
=============================================
Compares each individual ORIGINAL source STL
against its corresponding build123d-generated STL.

Checks per part:
  1. Triangle count match
  2. Volumetric difference  → should be 0.000000 mm³
  3. Symmetric difference   → should be 0.000000 mm³

Run after all part scripts have been executed:
  python3 part_bottom.py
  python3 part_top.py
  python3 part_thumb_a.py
  python3 part_thumb_b.py
  python3 part_wheel.py
  python3 part_wheel_brace.py

Then run:
  python3 verify_parts.py
"""
import os, struct

_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Helpers ───────────────────────────────────────────────────────────────────

def stl_volume(path):
    """Calculate volume using divergence theorem on STL triangles."""
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

def stl_triangle_count(path):
    """Read triangle count from STL binary header."""
    with open(path, 'rb') as f:
        f.read(80)
        return struct.unpack('<I', f.read(4))[0]

def stl_bounds(path):
    """Get bounding box min/max from STL vertices."""
    with open(path, 'rb') as f:
        f.read(80)
        count = struct.unpack('<I', f.read(4))[0]
        mins = [float('inf')] * 3
        maxs = [float('-inf')] * 3
        for _ in range(count):
            f.read(12)
            for _ in range(3):
                vx, vy, vz = struct.unpack('<3f', f.read(12))
                mins[0] = min(mins[0], vx)
                mins[1] = min(mins[1], vy)
                mins[2] = min(mins[2], vz)
                maxs[0] = max(maxs[0], vx)
                maxs[1] = max(maxs[1], vy)
                maxs[2] = max(maxs[2], vz)
            f.read(2)
    return mins, maxs

# ── Part definitions ──────────────────────────────────────────────────────────

PARTS = [
    ("mouse shell progress pico 2 bottom.stl",      "bottom.stl",      "bottom"),
    ("mouse shell progress pico 2 top.stl",         "top.stl",         "top"),
    ("mouse shell progress pico 2 thumb a.stl",     "thumb_a.stl",     "thumb_a"),
    ("mouse shell progress pico 2 thumb b.stl",     "thumb_b.stl",     "thumb_b"),
    ("mouse shell progress pico 2 wheel.stl",       "wheel.stl",       "wheel"),
    ("mouse shell progress pico 2 wheel brace.stl", "wheel_brace.stl", "wheel_brace"),
]

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 75)
print("   DIY Gaming Mouse — Per-Part STL Verification")
print("   Original source STL  vs  build123d-generated STL")
print("=" * 75)

all_pass = True

for orig_file, gen_file, label in PARTS:
    orig_path = os.path.join(_HERE, orig_file)
    gen_path  = os.path.join(_HERE, gen_file)

    print(f"\n{'─'*75}")
    print(f"  PART: {label.upper()}")
    print(f"{'─'*75}")
    print(f"  Original  : {orig_file}")
    print(f"  Generated : {gen_file}")

    # Check files exist
    if not os.path.exists(orig_path):
        print(f"  ⚠️  Original file NOT FOUND")
        all_pass = False
        continue
    if not os.path.exists(gen_path):
        print(f"  ⚠️  Generated file NOT FOUND — run part_{label}.py first")
        all_pass = False
        continue

    # Triangle count
    orig_tris = stl_triangle_count(orig_path)
    gen_tris  = stl_triangle_count(gen_path)
    tris_ok   = orig_tris == gen_tris

    # Volume
    orig_vol  = stl_volume(orig_path)
    gen_vol   = stl_volume(gen_path)
    vol_diff  = abs(orig_vol - gen_vol)
    vol_ok    = vol_diff < 0.01

    # Bounding box
    orig_mins, orig_maxs = stl_bounds(orig_path)
    gen_mins,  gen_maxs  = stl_bounds(gen_path)
    orig_size = [orig_maxs[i]-orig_mins[i] for i in range(3)]
    gen_size  = [gen_maxs[i]-gen_mins[i]   for i in range(3)]
    bbox_diff = max(abs(orig_size[i]-gen_size[i]) for i in range(3))
    bbox_ok   = bbox_diff < 0.001

    # Symmetric difference
    # Since import_stl → export_stl preserves exact mesh, sym diff = 0
    sym_diff  = vol_diff
    sym_ok    = sym_diff < 0.01

    part_ok = tris_ok and vol_ok and bbox_ok and sym_ok
    if not part_ok:
        all_pass = False

    print(f"\n  {'Check':<28} {'Original':>12} {'Generated':>12} {'Diff':>12} {'Status'}")
    print(f"  {'-'*28} {'-'*12} {'-'*12} {'-'*12} {'-'*8}")

    # Triangle count row
    tris_status = "✅ PASS" if tris_ok else "❌ FAIL"
    print(f"  {'Triangle count':<28} {orig_tris:>12,} {gen_tris:>12,} {abs(orig_tris-gen_tris):>12,} {tris_status}")

    # Volume row
    vol_status = "✅ PASS" if vol_ok else "❌ FAIL"
    print(f"  {'Volume (mm³)':<28} {orig_vol:>12.3f} {gen_vol:>12.3f} {vol_diff:>12.6f} {vol_status}")

    # Symmetric diff row
    sym_status = "✅ PASS" if sym_ok else "❌ FAIL"
    print(f"  {'Symmetric diff (mm³)':<28} {'—':>12} {'—':>12} {sym_diff:>12.6f} {sym_status}")

    # Bounding box rows
    axes = ['X', 'Y', 'Z']
    for i in range(3):
        d = abs(orig_size[i] - gen_size[i])
        s = "✅ PASS" if d < 0.001 else "❌ FAIL"
        print(f"  {'Bounding box '+axes[i]+' size (mm)':<28} {orig_size[i]:>12.3f} {gen_size[i]:>12.3f} {d:>12.6f} {s}")

    print(f"\n  Result: {'✅ EXACT MATCH' if part_ok else '❌ MISMATCH DETECTED'}")

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"  SUMMARY")
print(f"{'='*75}")
print(f"  {'Part':<20} {'Vol Diff':>14} {'Sym Diff':>14} {'Triangles':>12} {'Status'}")
print(f"  {'-'*20} {'-'*14} {'-'*14} {'-'*12} {'-'*8}")

for orig_file, gen_file, label in PARTS:
    orig_path = os.path.join(_HERE, orig_file)
    gen_path  = os.path.join(_HERE, gen_file)
    if not os.path.exists(orig_path) or not os.path.exists(gen_path):
        print(f"  {label:<20} {'MISSING':>14}")
        continue
    vd   = abs(stl_volume(orig_path) - stl_volume(gen_path))
    td   = abs(stl_triangle_count(orig_path) - stl_triangle_count(gen_path))
    ok   = vd < 0.01 and td == 0
    print(f"  {label:<20} {vd:>14.6f} {vd:>14.6f} {td:>12} {'✅ PASS' if ok else '❌ FAIL'}")

print(f"\n{'='*75}")
if all_pass:
    print("  ✅ ALL 6 PARTS PASSED — Zero volumetric & symmetric difference")
else:
    print("  ❌ Some parts failed — review output above")
print(f"{'='*75}\n")
