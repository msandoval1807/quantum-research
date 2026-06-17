"""
output_routing.py — automatically sort saved files into figures/ data/ movies/.

Usage (one line near the top of any notebook, with the project .venv active):

    from output_routing import route_outputs
    route_outputs()

After that, any save with a *bare* filename is sent to the folder that matches its
file type:

    plt.savefig("energy.png")              -> figures/energy.png
    fig.savefig("spectrum.pdf")            -> figures/spectrum.pdf
    np.save("trajectories", arr)           -> data/trajectories.npy
    imageio.mimsave("wigner.gif", frames)  -> movies/wigner.gif

Rules:
- Routing is by file extension (see _FOLDER_FOR_EXT below).
- A filename that already includes a folder ("figures/x.png", "C:/tmp/x.png") is left
  untouched, so existing organized code keeps working.
- The destination folders are created automatically.
- Calling route_outputs() more than once in a session is safe (it will not double-wrap).

This module lives in shared/ and is importable from any assignment folder via the
quantum_research_shared.pth entry in the virtual environment. It can also simply be
dropped into an assignment folder and imported the same way.
"""
import os

# Which folder each file type belongs in.
_FOLDER_FOR_EXT = {
    ".png": "figures", ".jpg": "figures", ".jpeg": "figures",
    ".pdf": "figures", ".svg": "figures", ".tif": "figures", ".tiff": "figures",
    ".npy": "data", ".npz": "data", ".csv": "data", ".txt": "data",
    ".gif": "movies", ".mp4": "movies", ".webm": "movies", ".avi": "movies", ".mov": "movies",
}

_DEFAULT_FOLDERS = ("figures", "data", "movies")
_PATCHED = False


def _route(name):
    """Prefix the right folder onto a bare filename based on its extension.

    Non-strings (file buffers, Path-like objects) and names that already contain a
    folder are returned unchanged.
    """
    if not isinstance(name, str):
        return name
    if os.path.dirname(name):                       # already has a folder -> leave alone
        return name
    folder = _FOLDER_FOR_EXT.get(os.path.splitext(name)[1].lower())
    if folder is None:                              # unknown type -> leave alone
        return name
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, name)


def route_outputs(folders=_DEFAULT_FOLDERS, verbose=True):
    """Create the output folders and make matplotlib/numpy/imageio saves auto-route."""
    global _PATCHED
    for d in folders:
        os.makedirs(d, exist_ok=True)
    if _PATCHED:
        if verbose:
            print("Output routing already active.")
        return

    # --- matplotlib: plt.savefig and Figure.savefig ---
    try:
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        _orig_savefig = plt.savefig
        def _savefig(fname, *a, **k):
            return _orig_savefig(_route(fname), *a, **k)
        plt.savefig = _savefig

        _orig_fig_savefig = Figure.savefig
        def _fig_savefig(self, fname, *a, **k):
            return _orig_fig_savefig(self, _route(fname), *a, **k)
        Figure.savefig = _fig_savefig
    except ImportError:
        pass

    # --- numpy: np.save (and np.savez) ---
    try:
        import numpy as np
        _orig_np_save = np.save
        def _np_save(file, *a, **k):
            if isinstance(file, str) and not os.path.dirname(file):
                if os.path.splitext(file)[1] == "":     # np.save adds .npy itself
                    file = file + ".npy"
                file = _route(file)
            return _orig_np_save(file, *a, **k)
        np.save = _np_save

        _orig_np_savez = np.savez
        def _np_savez(file, *a, **k):
            if isinstance(file, str) and not os.path.dirname(file):
                if os.path.splitext(file)[1] == "":
                    file = file + ".npz"
                file = _route(file)
            return _orig_np_savez(file, *a, **k)
        np.savez = _np_savez
    except ImportError:
        pass

    # --- imageio: mimsave / imwrite (for .gif, .mp4, image files) ---
    for modname in ("imageio", "imageio.v2"):
        try:
            mod = __import__(modname, fromlist=["dummy"])
        except ImportError:
            continue
        if hasattr(mod, "mimsave"):
            _orig_mimsave = mod.mimsave
            def _mimsave(uri, *a, _o=_orig_mimsave, **k):
                return _o(_route(uri), *a, **k)
            mod.mimsave = _mimsave
        if hasattr(mod, "imwrite"):
            _orig_imwrite = mod.imwrite
            def _imwrite(uri, *a, _o=_orig_imwrite, **k):
                return _o(_route(uri), *a, **k)
            mod.imwrite = _imwrite

    _PATCHED = True
    if verbose:
        print("Output routing active: images -> figures/, data -> data/, movies -> movies/")
