#!/usr/bin/env python3
"""
Create a local virtual environment for the Excel, Word, and bag-of-words
utilities in this repository.

Usage:
    python3 setup_environment.py

Optional:
    python3 setup_environment.py --python python3.11
    python3 setup_environment.py --venv .venv
"""

import argparse
import subprocess
import sys
from pathlib import Path


PACKAGES = [
    "pandas",
    "scikit-learn",
    "openpyxl",
    "pypandoc",
    "pypandoc_binary",
    "matplotlib",
]


def run(command, *, cwd=None):
    """Run a command and stop if it fails."""
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Create a virtual environment and install project dependencies."
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable to use (default: the Python running this script).",
    )
    parser.add_argument(
        "--venv",
        default="text_analysis_env",
        help="Virtual-environment directory (default: .venv).",
    )
    args = parser.parse_args()

    repo_dir = Path(__file__).resolve().parent
    venv_dir = Path(args.venv)
    if not venv_dir.is_absolute():
        venv_dir = repo_dir / venv_dir

    # Create the environment if it does not already exist.
    if not (venv_dir / "pyvenv.cfg").exists():
        run([args.python, "-m", "venv", str(venv_dir)])
    else:
        print(f"Using existing virtual environment: {venv_dir}")

    # Find the environment's Python executable (macOS/Linux or Windows).
    if sys.platform == "win32":
        env_python = venv_dir / "Scripts" / "python.exe"
    else:
        env_python = venv_dir / "bin" / "python"

    # Install and upgrade pip, then install dependencies.
    run([str(env_python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(env_python), "-m", "pip", "install", *PACKAGES])

    # Check imports and verify that Pandoc is available through pypandoc.
    check_code = (
        "import os, glob, pandas, sklearn, openpyxl, pypandoc; "
        "from sklearn.feature_extraction.text import CountVectorizer; "
        "print('Imports successful'); "
        "print('pandas:', pandas.__version__); "
        "print('scikit-learn:', sklearn.__version__); "
        "print('openpyxl:', openpyxl.__version__); "
        "print('Pandoc:', pypandoc.get_pandoc_version())"
    )
    run([str(env_python), "-c", check_code])

    print("\nEnvironment setup complete.")
    print(f"Environment directory: {venv_dir}")
    print("\nActivate it with:")
    if sys.platform == "win32":
        print(f'  "{venv_dir}\\Scripts\\activate"')
    else:
        try:
            relative_venv = venv_dir.relative_to(repo_dir)
            activation_path = f"./{relative_venv}/bin/activate"
        except ValueError:
            activation_path = str(venv_dir / "bin" / "activate")
        print(f"  source {activation_path}")
    print(
        "\nMake sure convert_to_txt.py is in your repository before running "
        "scripts that import it."
    )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(f"\nSetup failed (command exited with status {error.returncode}).", file=sys.stderr)
        sys.exit(error.returncode)
