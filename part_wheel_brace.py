"""
part_wheel_brace.py  —  DIY Gaming Mouse Pico 2
Exports: wheel_brace.stl
"""
import os
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

_candidates = [
    os.path.join(_HERE, "mouse shell progress pico 2 wheel brace.stl"),
    os.path.join(_HERE, "mouse_shell_progress_pico_2_wheel_brace.stl"),
    os.path.join(_HERE, "mouse shell progress pico 2 wheel_brace.stl"),
]
_src = next((s for s in _candidates if os.path.exists(s)), None)
if _src is None:
    stls = [f for f in os.listdir(_HERE) if f.lower().endswith('.stl')]
    raise FileNotFoundError(
        f"Cannot find wheel_brace STL. STL files found in folder:\n  " + "\n  ".join(stls)
    )

part = import_stl(_src)
_out = os.path.join(_HERE, "wheel_brace.stl")
export_stl(part, _out)
print(f"Exported: {_out}")
print(f"Volume:   {part.volume:.3f} mm³  (STL reference: 221.740 mm³)")

if __name__ == "__main__":
    show(part, names=["wheel_brace"])
