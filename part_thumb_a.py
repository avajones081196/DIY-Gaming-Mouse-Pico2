"""
part_thumb_a.py  —  DIY Gaming Mouse Pico 2
Exports: thumb_a.stl
"""
import os
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

_candidates = [
    os.path.join(_HERE, "mouse shell progress pico 2 thumb a.stl"),
    os.path.join(_HERE, "mouse_shell_progress_pico_2_thumb_a.stl"),
    os.path.join(_HERE, "mouse shell progress pico 2 thumb_a.stl"),
]
_src = next((s for s in _candidates if os.path.exists(s)), None)
if _src is None:
    # List what STL files ARE in the folder to help debug
    stls = [f for f in os.listdir(_HERE) if f.lower().endswith('.stl')]
    raise FileNotFoundError(
        f"Cannot find thumb_a STL. STL files found in folder:\n  " + "\n  ".join(stls)
    )

part = import_stl(_src)
_out = os.path.join(_HERE, "thumb_a.stl")
export_stl(part, _out)
print(f"Exported: {_out}")
print(f"Volume:   {part.volume:.3f} mm³  (STL reference: 896.408 mm³)")

if __name__ == "__main__":
    show(part, names=["thumb_a"])
