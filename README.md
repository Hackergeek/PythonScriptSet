# Python脚本集合

## kugou.py——获取酷狗TOP500歌曲信息

## tinypng

### 功能

使用tinypng批量压缩图片

### 用法

```bash
Usage: tinypng.py [OPTIONS]

Options:
  -f, --file TEXT      单个文件压缩
  -d, --dir TEXT       被压缩的文件夹
  -r, --recursive      是否递归遍历压缩
  -w, --width INTEGER  图片宽度，默认不变
  -o, --overwrite      是否覆盖原文件
  --help               Show this message and exit.
```

## videotranscoding

### 功能

使用ffmpeg批量视频转码，默认转为h265(hevc)，达到视频压缩的效果。
支持.mp4,.mkv,.mov这几种格式

### 用法

```bash
Usage: videotranscoding.py [OPTIONS] [FILE_LIST]...

Options:
  -r, --recursive       是否递归遍历转码
  -c, --codec TEXT      指定编码，默认为hevc(libx265)
  -o, --overwrite       是否覆盖原文件
  --help                Show this message and exit.
```
