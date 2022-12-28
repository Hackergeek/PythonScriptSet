#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import click
import sh
import ffmpeg_transcode as ffmpeg
import datetime
import time

version = "1.0.0"  # 版本
fileSuffixArray = ['.mp4', '.mkv', '.mov', '.flv']
success_count = 0
skip_count = 0
fail_list = []
total_count = 0
total_save_size = 0

# ffmpeg = sh.Command("/usr/local/bin/ffmpeg"))
# ffmpeg = sh.Command("ffmpeg")


def print_result():
    print("{} files have been processed, {} succeed, {} skipped, {} failure, save size:{}.".format(total_count, success_count, skip_count, len(fail_list), storage_format_size(total_save_size)))
    if len(fail_list) > 0:
        print("The following are details of the failure information:")
        for fail_file in fail_list:
            print(fail_file)

def transform_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time = "%02d:%02d:%02d" % (h, m, s)
    return time


def process_output(line, stdin, process):
    print(line, end='')
    if line is str and "ERROR" in line:
        process.kill()
        return True
    return False


def storage_format_size(size):
    kb_size = 1024
    mb_size = 1024 * kb_size
    gb_size = 1024 * mb_size
    if size >= gb_size:
        return str(round(size/gb_size, 2)) + "GB"
    if size >= mb_size:
        return str(round(size/mb_size, 2)) + "MB"
    else:
        return str(round(size/kb_size)) + "KB"       


# 转码的核心
def convert_core(input_file, output_file, codec):
    if os.path.exists(output_file):
        print("目标文件已存在")
        return False
    print("start convert %s" % input_file)
    global total_count
    global success_count
    total_count += 1
    # ffmpeg -i temp.mp4 -c:v libx265 -c:a copy temp1.h264
    before_convert_size = os.path.getsize(input_file)
    start_time = time.time()
    try:
        # process = ffmpeg("-i", inputFile, "-c:v", codec, "-threads", 4, "-c:a", "copy", outputFile, _out=process_output,
        #                  _err=process_output, _bg=True)  # ffmpeg的日志输出是stderr
        # process.wait()
        # result = ffmpeg.do_ffmpeg_transcode(f"ffmpeg -i {input_file} -c:v {codec} -threads 4 -c:a copy {output_file}")
        result = ffmpeg.do_ffmpeg_transcode(["ffmpeg", "-i", input_file, "-c:v", codec, "-threads", "8", "-c:a", "copy",
                                             output_file])
        if not result:
            print("The video encoding of the source file is consistent with that of the target file without transcoding")
            global skip_count
            skip_count += 1
            return result
        if os.path.exists(output_file):
            after_convert_size = os.path.getsize(output_file)
            end_time = time.time()
            success_count += 1
            save_size = before_convert_size - after_convert_size
            global total_save_size
            total_save_size += save_size
            print("\n convert finish save size:{}, cost time:{}".format(storage_format_size(save_size), transform_time(end_time - start_time)))
        return True
    except KeyboardInterrupt:
        os.remove(output_file)
        total_count -= 1
        print_result()
        print("\n键盘中断，程序运行结束")
        exit(-1)
    except Exception:
        fail_list.append(input_file)        

# 转码一个文件夹下的视频
def convert(path, codec, recursive, overwrite):
    if not os.path.isdir(path):
        convert_file(path, codec, overwrite)
        return
    fromFilePath = path  # 源路径
    print("fromFilePath=%s" % fromFilePath)
    for root, dirs, files in os.walk(fromFilePath):
        # print("root = %s" % root)
        # print("dirs = %s" % dirs)
        # print("files= %s" % files)

        for name in files:
            convert_file(root + os.path.sep + name, codec, overwrite)
        if not recursive:
            break


# 仅转码指定文件
def convert_file(input_file, codec, overwrite):
    if not os.path.isfile(input_file):
        print("这不是一个文件，请输入文件的正确路径!", input_file)
        return
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    fileName, fileSuffix = os.path.splitext(basename)
    fileSuffix = str(fileSuffix).lower()
    if fileSuffix in fileSuffixArray:
        # print("file = %s" % input_file)
        convert_output_file = dirname + '/convert_' + fileName + '.mp4'
        output_file = dirname + os.sep + fileName + '.mp4'
        
        result = convert_core(input_file, convert_output_file, codec) and os.path.exists(convert_output_file)
        if overwrite and result:
            os.remove(input_file)
            os.rename(convert_output_file, output_file)
        if not result and os.path.exists(convert_output_file) and os.path.getsize(convert_output_file) < 100:
            os.remove(convert_output_file)


@click.command()
@click.option('-r', "--recursive", is_flag=True, help="是否递归遍历转码")
@click.option('-c', "--codec", type=str, default="hevc", help="指定编码，默认为hevc(libx265)")
@click.option('-o', "--overwrite", is_flag=True, help="是否覆盖原文件")
@click.argument("file_list", nargs=-1, type=str, default=None)
def run(recursive, codec, overwrite, file_list):
    print("Skyward video transcoding V%s" % version)
    if len(file_list) > 0:
        for file in file_list:
            convert(file, codec, recursive, overwrite)  # 转码指定目录下的文件
    else:
        convert(os.getcwd(), codec, recursive, overwrite)  # 转码当前目录下的文件
    
    print_result()
    print("End!")


if __name__ == "__main__":
    run()
