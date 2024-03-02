import subprocess


def check_gh_auth():
    result = subprocess.run(["gh", "auth", "status"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return "Logged in to github.com" in output


# def run_git_command(command):
#     result = subprocess.run(command, stdout=subprocess.PIPE)
#     output = result.stdout.decode('utf-8')
#     return '\n'.join(output.split('\n')[:200])


def run_git_command(command, verbose=False):
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        raise Exception("Error executing command:", result.stderr)
    if verbose:
        print(result.stdout)
    return result.stdout
