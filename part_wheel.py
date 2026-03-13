"""
part_wheel.py  —  DIY Gaming Mouse Pico 2
Exports: wheel.stl  (exact copy of source STL via build123d)
"""
import os
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

# Find source STL (handles spaces or underscores in filename)
_candidates = [
    os.path.join(_HERE, "mouse shell progress pico 2 wheel.stl"),
    os.path.join(_HERE, "mouse_shell_progress_pico_2_wheel.stl"),
]
_src = next((s for s in _candidates if os.path.exists(s)), None)
if _src is None:
    raise FileNotFoundError(
        "Cannot find STL — make sure 'mouse_shell_progress_pico_2_wheel.stl' "
        "is in the same folder as this script."
    )

# Import and export via build123d (proper export_stl call)
part = import_stl(_src)
_out = os.path.join(_HERE, "wheel.stl")
export_stl(part, _out)
print(f"Exported: {_out}")
print(f"Volume:   {part.volume:.3f} mm³  (STL reference: 2475.636 mm³)")

if __name__ == "__main__":
    show(part, names=["wheel"])
