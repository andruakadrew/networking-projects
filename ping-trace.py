import os
import platform
import time
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from subprocess import check_output, CalledProcessError

CURRENT_DIR = os.getcwd()
START_TIME = time.time()
MAX_THREADS = 5
FILENAME = 'devices.txt'

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    PING_COMMAND = 'ping -n 3 -w 1000'
    TRACEROUTE_COMMAND = 'tracert'
else:
    PING_COMMAND = 'ping -q -c 3 -W 1'
    TRACEROUTE_COMMAND = 'traceroute'

formatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, format=formatter, level=logging.DEBUG)


def title(section_name):
    section_title = '\n' + '*' * 70 + f'\n{section_name}\n' + '*' * 70 + '\n'
    return section_title


def health_checks(ip):
    ping_cmd = f'{PING_COMMAND} {ip}'
    trace_cmd = f'{TRACEROUTE_COMMAND} {ip}'

    ping_status = run_command(ping_cmd)
    trace_status = run_command(trace_cmd)

    filename = f'{CURRENT_DIR}{os.sep}{ip}.txt'
    with open(filename, 'w') as f:
        f.write(title('Ping Results:'))
        f.write(ping_status)
        f.write(title('Trace Results:'))
        f.write(trace_status)

    logging.info(f'Wrote outputs to: {filename}')
    logging.debug(ping_status)
    logging.debug(trace_status)


def run_command(command):
    logging.info(f'running: {command}')
    split_cmd = command.split()
    try:
        output = check_output(split_cmd, stderr=-2).decode('utf-8')
    except CalledProcessError:
        return 'FAILED'
    except FileNotFoundError:
        return f'ERROR: command not found — {split_cmd[0]}'
    return output


def main():
    with open(FILENAME, 'r') as f:
        ips = f.read().splitlines()
        num_ips = len(ips)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        [executor.submit(health_checks, ip) for ip in ips]

    end_time = time.time() - START_TIME
    logging.info(f'Checked {num_ips} hosts in {round(end_time)} seconds.')


if __name__ == '__main__':
    main()