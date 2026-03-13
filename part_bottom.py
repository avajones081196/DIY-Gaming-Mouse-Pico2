"""
part_bottom.py  —  DIY Gaming Mouse Pico 2
Exports: bottom.stl  (exact copy of source STL via build123d)
"""
import os
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

_candidates = [
    os.path.join(_HERE, "mouse shell progress pico 2 bottom.stl"),
    os.path.join(_HERE, "mouse_shell_progress_pico_2_bottom.stl"),
]
_src = next((s for s in _candidates if os.path.exists(s)), None)
if _src is None:
    raise FileNotFoundError(
        "Cannot find STL — make sure 'mouse_shell_progress_pico_2_bottom.stl' "
        "is in the same folder as this script."
    )

part = import_stl(_src)
_out = os.path.join(_HERE, "bottom.stl")
export_stl(part, _out)
print(f"Exported: {_out}")
print(f"Volume:   {part.volume:.3f} mm³  (STL reference: 14154.497 mm³)")

if __name__ == "__main__":
    show(part, names=["bottom"])
