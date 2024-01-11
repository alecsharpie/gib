import subprocess

def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return '\n'.join(output.split('\n')[:200])
