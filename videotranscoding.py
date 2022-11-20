#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import click
import sh
import ffmpeg_transcode as ffmpeg

version = "1.0.0"  # 版本
fileSuffixArray = ['.mp4', '.h264']


# ffmpeg = sh.Command("/usr/local/bin/ffmpeg"))
# ffmpeg = sh.Command("ffmpeg")


def process_output(line, stdin, process):
    print(line, end='')
    if line is str and "ERROR" in line:
        process.kill()
        return True
    return False


# 转码的核心
def compress_core(input_file, output_file, codec):
    print("start convert %s" % input_file)
    # ffmpeg -i temp.mp4 -c:v libx265 -c:a copy temp1.h264
    before_convert_size = os.path.getsize(input_file)
    try:
        # process = ffmpeg("-i", inputFile, "-c:v", codec, "-threads", 4, "-c:a", "copy", outputFile, _out=process_output,
        #                  _err=process_output, _bg=True)  # ffmpeg的日志输出是stderr
        # process.wait()
        ffmpeg.do_ffmpeg_transcode(f'ffmpeg -i {input_file} -c:v {codec} -threads 4 -c:a copy {output_file}')
        after_convert_size = os.path.getsize(output_file)
        print("convert finish save %sKB" % ((before_convert_size - after_convert_size) / 1024))
        return True
    except sh.ErrorReturnCode_1:
        os.remove(output_file)
        return False


# 转码一个文件夹下的视频
def convert_path(path, codec, recursive, overwrite):
    print("compress_path-------------------------------------")
    if not os.path.isdir(path):
        print("这不是一个文件夹，请输入文件夹的正确路径!")
        return
    else:
        fromFilePath = path  # 源路径
        print("fromFilePath=%s" % fromFilePath)

        for root, dirs, files in os.walk(fromFilePath):
            # print("root = %s" % root)
            # print("dirs = %s" % dirs)
            # print("files= %s" % files)

            for name in files:
                fileName, fileSuffix = os.path.splitext(name)
                fileSuffix = str(fileSuffix).lower()
                if fileSuffix in fileSuffixArray:
                    inputFile = root + '/' + name
                    if not overwrite:
                        toFilePath = root + "/convert"  # 输出路径
                        # print("toFilePath=%s" % toFilePath)
                        outputFile = toFilePath + '/' + name
                        if os.path.isdir(toFilePath):
                            pass
                        else:
                            os.mkdir(toFilePath)
                        compress_core(inputFile, outputFile, codec)
                    else:
                        outputFile = root + '/temp_' + name
                        if compress_core(inputFile, outputFile, codec):
                            os.remove(inputFile)
                            os.rename(outputFile, inputFile)
            if not recursive:
                break  # 仅遍历当前目录


# 仅转码指定文件
def convert_file(input_file, codec, overwrite):
    print("compress_file-------------------------------------")
    if not os.path.isfile(input_file):
        print("这不是一个文件，请输入文件的正确路径!")
        return
    print("file = %s" % input_file)
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    fileName, fileSuffix = os.path.splitext(basename)
    fileSuffix = str(fileSuffix).lower()
    if fileSuffix in fileSuffixArray:
        if overwrite:
            outputFile = dirname + '/temp_' + basename
            if compress_core(input_file, outputFile, codec):
                os.remove(input_file)
                os.rename(outputFile, input_file)
        else:
            compress_core(input_file, dirname + "/convert_" + basename, codec)
    else:
        print("不支持该文件类型!")


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件转码")
@click.option('-d', "--directory", type=str, default=None, help="被转码的文件夹")
@click.option('-r', "--recursive", is_flag=True, help="是否递归遍历转码")
@click.option('-c', "--codec", type=str, default="libx265", help="指定编码，默认为libx265")
@click.option('-o', "--overwrite", is_flag=True, help="是否覆盖原文件")
def run(file, directory, recursive, codec, overwrite):
    print("Skyward video transcoding V%s" % version)
    if file is not None:
        convert_file(file, codec, overwrite)  # 仅转码一个文件
        pass
    elif directory is not None:
        convert_path(directory, codec, recursive, overwrite)  # 转码指定目录下的文件
        pass
    else:
        convert_path(os.getcwd(), codec, recursive, overwrite)  # 转码当前目录下的文件
    print("结束!")


if __name__ == "__main__":
    run()
