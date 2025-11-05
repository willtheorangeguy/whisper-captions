
import glob
import subprocess
import os

# Get the directory of the current script (loop.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find all .mp4 files in the current directory
mp4_files = glob.glob(os.path.join(script_dir, "*.mp4"))

# Path to cli.py
cli_script_path = os.path.join(script_dir, "cli.py")

for mp4_file in mp4_files:
    print(f"Processing {mp4_file}...")
    command = ["python", cli_script_path, mp4_file]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully processed {mp4_file}")
        print("Stdout:", result.stdout)
        if result.stderr:
            print("Stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error processing {mp4_file}: {e}")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
    except FileNotFoundError:
        print(f"Error: python or cli.py not found. Make sure python is in your PATH and cli.py exists at {cli_script_path}")
    print("-" * 30)
