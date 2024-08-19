import os


def restart_script():
    # Get the current script path
    script_path = os.path.abspath(__file__)

    # Use os.system to call the script again
    os.system(f'python {script_path}')


def handle_command(command):
    if command == 'restart':
        restart_script()

