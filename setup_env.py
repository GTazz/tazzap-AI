import os
import subprocess
import sys
import venv

# --- Configuration ---
# get current path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
# set env_dir to the current path + env
ENV_DIR = os.path.join(PROJECT_PATH, "env")
REQUIREMENTS_FILE = "requirements.txt"
# --- End Configuration ---

def get_pip_path(env_dir):
    """Gets the path to the pip executable within the virtual environment."""
    if sys.platform == "win32":
        return os.path.join(env_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(env_dir, "bin", "pip")

def main():
    """Main function to create the environment and install dependencies."""
    print(f"Checking/Creating virtual environment in: {ENV_DIR}")

    # Create the virtual environment if it doesn't exist
    if not os.path.exists(ENV_DIR):
        try:
            print("Creating virtual environment...")
            venv.create(ENV_DIR, with_pip=True)
            print("Virtual environment created successfully.")
        except Exception as e:
            print(f"Error creating virtual environment: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Virtual environment already exists.")

    # Find the path to pip in the virtual environment
    pip_executable = get_pip_path(ENV_DIR)

    if not os.path.exists(pip_executable):
        print(f"Error: Pip executable not found at {pip_executable}", file=sys.stderr)
        print("Try recreating the virtual environment (remove the 'env' folder and run the script again).", file=sys.stderr)
        sys.exit(1)

    # Check if the requirements.txt file exists
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"Warning: File '{REQUIREMENTS_FILE}' not found. No dependencies will be installed.")
    else:
        print(f"Installing dependencies from {REQUIREMENTS_FILE} using {pip_executable}...")
        try:
            # Install dependencies using pip from the virtual environment
            # Use capture_output=True and text=True for better error handling in Python 3.7+
            subprocess.run([pip_executable, "install", "-r", REQUIREMENTS_FILE], check=True, capture_output=True, text=True, encoding='utf-8')
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error installing dependencies:", file=sys.stderr)
            # Print stderr for detailed error messages
            print(e.stderr, file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
             print(f"Error: The command '{pip_executable}' was not found.", file=sys.stderr)
             print("Verify that the virtual environment was created correctly.", file=sys.stderr)
             sys.exit(1)


    print("\n--- Setup Complete ---")
    print("To activate the virtual environment, run:")
    if sys.platform == "win32":
        print(f"In CMD: .\\{ENV_DIR}\\Scripts\\activate.bat")
        print(f"In PowerShell: .\\{ENV_DIR}\\Scripts\\Activate.ps1")
        print(" (You might need to adjust the execution policy: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser)\n")
    else:
        print(f"In Bash/Zsh: source ./{ENV_DIR}/bin/activate\n")

if __name__ == "__main__":
    main()
