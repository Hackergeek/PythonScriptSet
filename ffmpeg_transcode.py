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


def do_ffmpeg_transcode_cmd(cmd):
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, bufsize=0, universal_newlines=True, shell=True)
    return compute_progress_and_send_progress(process)


def do_ffmpeg_transcode(args=[]):
    process = subprocess.Popen(args, stderr=subprocess.PIPE, bufsize=0, universal_newlines=True, shell=False)
    return compute_progress_and_send_progress(process)


def print_progress(progress):
    print("\r进度:{}%:".format(round(progress, 2)), "▓" * math.ceil(progress), end='')
    sys.stdout.flush()


def compute_progress_and_send_progress(process):
    duration = None
    input_codec = None
    output_codec = None
    while process.poll() is None:
        line = process.stderr.readline().strip()
        if line:
            # print(line)
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            codec_res = re.search(r'Video: (?P<video>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)
            # TODO 支持多路视频流，目前只支持一路视频流的判断
            if codec_res is not None:
                if input_codec is None:
                    input_codec = codec_res.groupdict()['video']
                else:
                    output_codec = codec_res.groupdict()['video']
            if input_codec is not None and input_codec == output_codec:
                # print("源文件视频编码与目标文件视频编码一致，无需转码")
                process.kill()
                return False

            result = re.search(r'time=(?P<time>\S+)', line)
            if result is not None and duration is not None:
                elapsed_time = result.groupdict()['time']

                currentTime = get_seconds(elapsed_time)
                allTime = get_seconds(duration)
                progress = currentTime * 100 / allTime
                print_progress(progress)
    return True


do_ffmpeg_transcode_cmd("ffmpeg -i 1.mp4 -c:v hevc -c:a copy 2.mp4")