#!/bin/bash

# 定义变量
GLIBC_DIR="$HOME/glibc-all-in-one"
GLIBC_URL="https://example.com/glibc-all-in-one.tar.gz" # 替换为实际的下载链接
PATCHELF_URL="https://github.com/NixOS/patchelf/archive/refs/tags/0.13.tar.gz" # 替换为实际的下载链接

# 检查glibc-all-in-one是否存在
if [ ! -d "$GLIBC_DIR" ]; then
  echo "glibc-all-in-one not found in home directory. Installing..."
  mkdir -p "$GLIBC_DIR"
  wget -O /tmp/glibc-all-in-one.tar.gz "$GLIBC_URL" || { echo "Failed to download glibc-all-in-one"; exit 1; }
  tar -xzvf /tmp/glibc-all-in-one.tar.gz -C "$GLIBC_DIR" --strip-components=1 || { echo "Failed to extract glibc-all-in-one"; exit 1; }
  echo "glibc-all-in-one installed successfully."
else
  echo "glibc-all-in-one already exists in home directory."
fi

# 检查patchelf是否已安装
if ! command -v patchelf &> /dev/null; then
  echo "patchelf not found. Installing..."
  wget -O /tmp/patchelf.tar.gz "$PATCHELF_URL" || { echo "Failed to download patchelf"; exit 1; }
  tar -xzvf /tmp/patchelf.tar.gz -C /tmp || { echo "Failed to extract patchelf"; exit 1; }
  cd /tmp/patchelf-* || { echo "Failed to enter patchelf directory"; exit 1; }
  ./bootstrap.sh || { echo "Bootstrap failed"; exit 1; }
  ./configure || { echo "Configure failed"; exit 1; }
  make || { echo "Make failed"; exit 1; }
  sudo make install || { echo "Make install failed"; exit 1; }
  echo "patchelf installed successfully."
else
  echo "patchelf is already installed."
fi

# 清理临时文件
rm -rf /tmp/glibc-all-in-one.tar.gz /tmp/patchelf.tar.gz /tmp/patchelf-*

echo "All tasks completed successfully."