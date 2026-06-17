"""
group_plot_style.py — one-line enforcement of the group's plotting standards.

Usage in every notebook, right after imports:

    from group_plot_style import apply_group_style
    apply_group_style()

Why this exists: the group requires labeled axes, legible fonts on slides, and
perceptually uniform colormaps. Setting matplotlib defaults once means every
figure follows the rules automatically instead of you remembering each time.
"""

import matplotlib.pyplot as plt
from cycler import cycler


def apply_group_style():
    """Set matplotlib defaults to meet the group's figure standards."""
    plt.rcParams.update({
        # --- fonts sized for slides (tick labels stay legible when scaled) ---
        "font.size": 14,
        "axes.labelsize": 16,
        "axes.titlesize": 16,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 13,

        # --- perceptually uniform colormap as the default for images/contours ---
        "image.cmap": "viridis",

        # --- distinguishable line colors sampled from viridis ---
        "axes.prop_cycle": cycler(color=plt.get_cmap("viridis")([0.0, 0.25, 0.5, 0.75, 0.95])),

        # --- clean, readable axes ---
        "lines.linewidth": 2.0,
        "axes.grid": True,
        "grid.alpha": 0.3,

        # --- sharp figures on screen and in exported slides ---
        "figure.dpi": 110,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def labeled_figure(xlabel, ylabel, title=None, figsize=(7, 5)):
    """Create a figure whose axes start out labeled — so no figure ships bare.

    Example:
        fig, ax = labeled_figure("position x (dimensionless)", "momentum p (dimensionless)")
    """
    figure, axes = plt.subplots(figsize=figsize)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    if title:
        axes.set_title(title)
    return figure, axes
