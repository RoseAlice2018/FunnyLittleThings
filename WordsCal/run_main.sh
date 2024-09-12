#!/bin/bash

MAIN_PATH = "./main"
LOG_FILE = "./excute.log"

if [- x "$MAIN_PATH"]; then
    echo "正在执行程序： $MAIN_PATH"
    "$MAIN_PATH" >> "$LOG_FILE" 2>&1
else 
    echo "错误: 程序 $MAIN_PATH 不存在或不可执行" >> "$LOG_FILE"
fi 