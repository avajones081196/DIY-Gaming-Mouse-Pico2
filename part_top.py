"""
part_top.py  —  DIY Gaming Mouse Pico 2
Exports: top.stl  (exact copy of source STL via build123d)
"""
import os
from build123d import *
from ocp_vscode import show

_HERE = os.path.dirname(os.path.abspath(__file__))

_candidates = [
    os.path.join(_HERE, "mouse shell progress pico 2 top.stl"),
    os.path.join(_HERE, "mouse_shell_progress_pico_2_top.stl"),
]
_src = next((s for s in _candidates if os.path.exists(s)), None)
if _src is None:
    raise FileNotFoundError(
        "Cannot find STL — make sure 'mouse_shell_progress_pico_2_top.stl' "
        "is in the same folder as this script."
    )

part = import_stl(_src)
_out = os.path.join(_HERE, "top.stl")
export_stl(part, _out)
print(f"Exported: {_out}")
print(f"Volume:   {part.volume:.3f} mm³  (STL reference: 9210.121 mm³)")

if __name__ == "__main__":
    show(part, names=["top"])
