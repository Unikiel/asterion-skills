#!/usr/bin/env python3
"""Run shared and subskill test suites from any working directory."""
import os
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    directories = [root / 'scripts', *sorted((root / 'subskills').glob('*/scripts'))]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for directory in directories:
        print(f'Testing {directory.relative_to(root).as_posix()}', flush=True)
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(directory),
                                 '-p', 'test_*.py'], env=environment)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
