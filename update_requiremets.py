import subprocess
import sys
import os

# get current path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
# set env_dir to the current path + env
ENV_DIR = os.path.join(PROJECT_PATH, "env")

def get_py_path(env_dir):
    """Gets the path to the Python executable within the virtual environment."""
    if sys.platform == "win32":
        return os.path.join(env_dir, "Scripts", "python.exe")
    else:
        return os.path.join(env_dir, "bin", "python")

def update_requirements():
    """
    Gets the current Python version and installed packages (pip freeze)
    and writes them to requirements.txt.
    """
    try:
        # Get Python version from the virtual environment
        py_executable = get_py_path(ENV_DIR)
        result = subprocess.run([py_executable, '-c', 'import sys; print(f\"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\")'], capture_output=True, text=True, check=True)
        python_version = result.stdout.strip()
        python_version_comment = f"# Python {python_version}\n"

        # Get installed packages using pip freeze
        result = subprocess.run([py_executable, '-m', 'pip', 'freeze'], capture_output=True, text=True, check=True)
        packages = result.stdout

        # Define the requirements file path relative to the script
        script_dir = os.path.dirname(__file__)
        requirements_path = os.path.join(script_dir, 'requirements.txt')


        # Write to requirements.txt
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(python_version_comment)
            f.write(packages)

        print(f"Successfully updated {requirements_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze: {e}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_requirements()
    