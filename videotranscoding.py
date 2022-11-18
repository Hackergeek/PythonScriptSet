#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import click
import sh

version = "1.0.0"  # 版本
fileSuffixArray = ['.mp4', '.h264']
# ffmpeg = sh.Command("/usr/local/bin/ffmpeg"))
ffmpeg = sh.Command("ffmpeg")


def process_output(line, stdin, process):
    print(line, end='')
    if "ERROR" in line:
        process.kill()
        return True


# 转码的核心
def compress_core(inputFile, outputFile, codec):
    print("start convert %s" % inputFile)
    #ffmpeg -i temp.mp4 -c:v libx265 -c:a copy temp1.h264
    before_convert_size = os.path.getsize(inputFile)
    process = ffmpeg("-i", inputFile, "-c:v", codec, "-c:a", "copy", outputFile, _out=process_output,
                     _err=process_output, _bg=True)
    process.wait()
    after_convert_size = os.path.getsize(outputFile)
    print("convert finish save %sKB" % ((before_convert_size-after_convert_size)/1024))


# 压缩一个文件夹下的图片
def convert_path(path, codec, recursive, overwrite):
    print("compress_path-------------------------------------")
    if not os.path.isdir(path):
        print("这不是一个文件夹，请输入文件夹的正确路径!")
        return
    else:
        fromFilePath = path  # 源路径
        toFilePath = path + "/tiny"  # 输出路径
        print("fromFilePath=%s" % fromFilePath)
        print("toFilePath=%s" % toFilePath)

        for root, dirs, files in os.walk(fromFilePath):
            print("root = %s" % root)
            print("dirs = %s" % dirs)
            print("files= %s" % files)
            for name in files:
                fileName, fileSuffix = os.path.splitext(name)
                fileSuffix = str(fileSuffix).lower()
                if fileSuffix in fileSuffixArray:
                    inputFile = root + '/' + name
                    outputFile = inputFile
                    if not overwrite:
                        toFullPath = toFilePath + root[len(fromFilePath):]
                        outputFile = toFullPath + '/' + name
                        if os.path.isdir(toFullPath):
                            pass
                        else:
                            os.mkdir(toFullPath)
                    compress_core(inputFile, outputFile, codec)
            if not recursive:
                break  # 仅遍历当前目录


# 仅压缩指定文件
def convert_file(inputFile, codec, overwrite):
    print("compress_file-------------------------------------")
    if not os.path.isfile(inputFile):
        print("这不是一个文件，请输入文件的正确路径!")
        return
    print("file = %s" % inputFile)
    dirname = os.path.dirname(inputFile)
    basename = os.path.basename(inputFile)
    fileName, fileSuffix = os.path.splitext(basename)
    fileSuffix = str(fileSuffix).lower()
    if fileSuffix in fileSuffixArray:
        if overwrite:
            compress_core(inputFile, inputFile, codec)
        else:
            compress_core(inputFile, dirname + "/tiny_" + basename, codec)
    else:
        print("不支持该文件类型!")


@click.command()
@click.option('-f', "--file", type=str, default=None, help="单个文件转码")
@click.option('-d', "--directory", type=str, default=None, help="被转码的文件夹")
@click.option('-r', "--recursive", is_flag=True, help="是否递归遍历转码")
@click.option('-c', "--codec", type=str, default="libx265", help="指定编码，默认为libx265")
# @click.option('-o', "--overwrite", is_flag=True, help="是否覆盖原文件")
def run(file, directory, recursive, codec, overwrite=None):
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
