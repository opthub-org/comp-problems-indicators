"""Utilities for Docker."""

import json
import subprocess
from typing import Any

import docker


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


def executor(image_name: str, environment: dict[str, object], std_in: str, timeout: int) -> dict[str, Any] | None:
    """Run the Docker image.

    Args:
        image_name (str): image name
        environment (dict[str, object]): environment variables
        std_in (str): stdin for the Docker image
        timeout (int): timeout

    Returns:
        dict[str, Any] | None: stdout
    """
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        environment=environment,
        stdin_open=True,
        detach=True,
    )
    socket = container.attach_socket(params={"stdin": 1, "stream": 1, "stdout": 1, "stderr": 1})
    for line in std_in:
        socket._sock.sendall(line.encode("utf-8"))  # noqa: SLF001
    container.wait(timeout=timeout)

    stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
    parsed_stdout = parse_stdout(stdout)

    container.remove()

    return parsed_stdout


def parse_stdout(stdout: str) -> dict[str, Any] | None:
    """Parse stdout.

    Args:
        stdout (str): stdout

    Returns:
        dict[str, Any] | None: parsed stdout
    """
    lines = stdout.split("\n")
    lines.reverse()
    for line in lines:
        if line:
            line_dict: dict[str, Any] = json.loads(line)
            return line_dict
    return None
