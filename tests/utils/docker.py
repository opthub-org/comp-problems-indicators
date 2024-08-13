"""Utilities for Docker."""

import subprocess


def build_image_on_subprocess(image_type: str, name: str) -> None:
    """Build the Docker image.

    Args:
        image_type (str): problem or indicator
        name (str): problem or indicator name
    """
    subprocess.run(["make", f"build-{image_type}", f"NAME={name}"], check=True)  # Build the image  # noqa: S603, S607
    subprocess.run(["docker", "image", "prune", "-f"], check=True)  # Delete <none> images  # noqa: S603, S607


def build_image(image_type: str, name: str) -> str:
    """Build the Docker image and return the image_name.

    Args:
        image_type (str): problem or indicator
        name (str): problem or indicator name
    """
    build_image_on_subprocess(image_type, name)
    return f"opthub/{image_type}-{name}:latest"
