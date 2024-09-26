"""Visualize the function."""

import matplotlib.pyplot as plt
import numpy as np

from opthub_problems.sphere.evaluator import evaluate


def visualization() -> None:
    """Visualize the sphere function."""
    file = "opthub_problems/sphere/sphere.jpg"
    opt = [[0.0, 0.0]]

    x = np.linspace(-5, 5, 200)
    y = np.linspace(-5, 5, 200)
    x, y = np.meshgrid(x, y)

    var_list = np.column_stack([x.ravel(), y.ravel()]).tolist()

    z = np.array([evaluate(var, opt)["objective"] for var in var_list])
    z = z.reshape(x.shape)

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x, y, z, cmap="rainbow", edgecolor="none")  # type: ignore[attr-defined]

    plt.subplots_adjust(left=-0.2, right=1.2, top=1.2, bottom=-0.2)
    ax.view_init(elev=25, azim=125)  # type: ignore[attr-defined]
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])  # type: ignore[attr-defined]

    plt.savefig(file, format="jpg", dpi=600)
    plt.close()


visualization()
