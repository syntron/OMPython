import subprocess

print('START')

cmd = ['sleep', '30s']
seconds = 2

try:
    output = subprocess.run(cmd, stderr=subprocess.STDOUT, timeout=seconds)
except subprocess.TimeoutExpired as ex:
    print(f'Timeout: {ex} {type(ex)}')

print('Done')
