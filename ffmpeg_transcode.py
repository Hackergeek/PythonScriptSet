import math
import re
import subprocess
import sys


def get_seconds(time):
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts


def do_ffmpeg_transcode(cmd):
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, bufsize=0, universal_newlines=True, shell=True)
    compute_progress_and_send_progress(process)


def print_progress(progress):
    print("\r进度:{:.2f}%:".format(progress), "▓" * math.ceil(progress), end="")
    sys.stdout.flush()


def compute_progress_and_send_progress(process):
    duration = None
    while process.poll() is None:
        line = process.stderr.readline().strip()
        if line:
            # print(line)
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)

            result = re.search(r'time=(?P<time>\S+)', line)
            if result is not None and duration is not None:
                elapsed_time = result.groupdict()['time']

                currentTime = get_seconds(elapsed_time)
                allTime = get_seconds(duration)
                progress = currentTime * 100 / allTime
                print_progress(progress)

# do_ffmpeg_transcode("ffmpeg -i 1.mp4 -c:v hevc -c:a copy 2.mp4")
