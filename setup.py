"""
Setup script for chatbot API testing framework.
Handles OneDrive path issues and provides clear feedback.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and provide feedback."""
    print(f"\n{'='*60}")
    print(f"⏳ {description}...")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def main():
    print(
        """
    ╔════════════════════════════════════════════════════════╗
    ║   Chatbot API Testing Framework - Setup Script        ║
    ╚════════════════════════════════════════════════════════╝
    """
    )

    # Check Python version
    print(f"Python version: {sys.version}")

    # Create reports directory
    reports_dir = Path("reports")
    if not reports_dir.exists():
        reports_dir.mkdir()
        print("✅ Created reports directory")

    # Install dependencies directly (skip venv for now due to OneDrive issues)
    print("\n" + "=" * 60)
    print("Installing dependencies...")
    print("=" * 60)
    print("\n⚠️  Note: Installing globally due to OneDrive path limitations.")
    print("You can create a venv manually later if needed.\n")

    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"
    ):
        print("\n❌ Failed to install dependencies")
        return False

    # Run smoke tests
    if not run_command(f"{sys.executable} -m pytest -v -m smoke", "Running smoke tests"):
        print("\n⚠️  Some tests failed, but setup is complete")

    print(
        """
    ╔════════════════════════════════════════════════════════╗
    ║              Setup Complete! 🎉                        ║
    ╚════════════════════════════════════════════════════════╝
    
    Next steps:
    
    1. Run all tests:
       python -m pytest -v
    
    2. Run quality tests:
       python -m pytest -v -m quality
    
    3. Generate HTML report:
       python -m pytest --html=reports/report.html --self-contained-html
    
    4. Test the quality scorer:
       python test_quality.py
    
    5. Adjust quality threshold (optional):
       Set QUALITY_THRESHOLD in .env file
    
    📖 See README.md for complete documentation
    """
    )

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
