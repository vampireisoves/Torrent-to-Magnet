#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Torrent种子文件转Magnet磁力链接工具
"""

import sys
import os
import hashlib
import bencodepy
from urllib.parse import quote


class TorrentToMagnet:
    """Torrent转Magnet转换器"""

    def __init__(self, torrent_path):
        self.torrent_path = torrent_path
        self.torrent_data = None
        self.info_hash = None
        self.name = None
        self.trackers = []
        self.total_size = 0

    def load_torrent(self):
        """加载并解析torrent文件"""
        try:
            with open(self.torrent_path, 'rb') as f:
                self.torrent_data = bencodepy.decode(f.read())
            return True
        except Exception as e:
            print(f"错误: 无法加载torrent文件 - {e}")
            return False

    def calculate_info_hash(self):
        """计算info hash"""
        try:
            info = self.torrent_data.get(b'info')
            if not info:
                print("错误: torrent文件中缺少info字段")
                return False

            # 编码info部分
            encoded_info = bencodepy.encode(info)
            # 计算SHA1哈希
            sha1 = hashlib.sha1(encoded_info)
            self.info_hash = sha1.hexdigest()
            return True
        except Exception as e:
            print(f"错误: 计算info hash失败 - {e}")
            return False

    def extract_metadata(self):
        """提取元数据"""
        try:
            info = self.torrent_data.get(b'info', {})

            # 提取名称
            name = info.get(b'name', b'Unknown')
            self.name = name.decode('utf-8', errors='ignore')

            # 提取tracker列表
            # 可能的tracker位置: announce, announce-list
            announce = self.torrent_data.get(b'announce')
            if announce:
                self.trackers.append(announce.decode('utf-8', errors='ignore'))

            announce_list = self.torrent_data.get(b'announce-list')
            if announce_list:
                for tracker_list in announce_list:
                    for tracker in tracker_list:
                        tracker_str = tracker.decode('utf-8', errors='ignore')
                        if tracker_str not in self.trackers:
                            self.trackers.append(tracker_str)

            # 计算总大小
            if b'length' in info:
                # 单文件
                self.total_size = info.get(b'length', 0)
            elif b'files' in info:
                # 多文件
                for file_info in info.get(b'files', []):
                    self.total_size += file_info.get(b'length', 0)

            return True
        except Exception as e:
            print(f"错误: 提取元数据失败 - {e}")
            return False

    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def generate_magnet(self):
        """生成magnet链接"""
        if not self.info_hash or not self.name:
            return None

        magnet_parts = [f"magnet:?xt=urn:btih:{self.info_hash}"]
        magnet_parts.append(f"&dn={quote(self.name)}")

        # 添加tracker
        for tracker in self.trackers[:5]:  # 最多添加5个tracker
            magnet_parts.append(f"&tr={quote(tracker)}")

        # 添加文件大小（可选）
        if self.total_size > 0:
            magnet_parts.append(f"&xl={self.total_size}")

        return ''.join(magnet_parts)

    def convert(self):
        """执行转换"""
        print(f"\n正在处理: {os.path.basename(self.torrent_path)}")
        print("-" * 60)

        # 加载torrent文件
        if not self.load_torrent():
            return None

        # 计算info hash
        if not self.calculate_info_hash():
            return None

        # 提取元数据
        if not self.extract_metadata():
            return None

        # 生成magnet链接
        magnet = self.generate_magnet()

        # 显示信息
        print(f"名称: {self.name}")
        print(f"大小: {self.format_size(self.total_size)}")
        print(f"Info Hash: {self.info_hash}")
        print(f"Tracker数量: {len(self.trackers)}")

        return magnet


def copy_to_clipboard(text):
    """复制文本到剪贴板"""
    try:
        import pyperclip
        pyperclip.copy(text)
        print("\n✓ Magnet链接已复制到剪贴板")
        return True
    except ImportError:
        print("\n提示: 安装pyperclip库可自动复制到剪贴板")
        print("      运行: pip install pyperclip")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Torrent转Magnet工具 v1.0")
        print("=" * 60)
        print("\n使用方法:")
        print("  1. 拖拽torrent文件到此exe上")
        print("  2. 或在命令行中执行: torrent_to_magnet.exe <torrent文件路径>")
        print("\n示例:")
        print("  torrent_to_magnet.exe movie.torrent")
        print("  torrent_to_magnet.exe *.torrent")
        sys.exit(0)

    # 获取文件列表
    file_paths = []
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            if arg.endswith('.torrent'):
                file_paths.append(arg)
            else:
                print(f"警告: 跳过非torrent文件: {arg}")
        elif os.path.isdir(arg):
            # 如果是目录，查找其中的torrent文件
            for root, dirs, files in os.walk(arg):
                for file in files:
                    if file.endswith('.torrent'):
                        file_paths.append(os.path.join(root, file))

    if not file_paths:
        print("错误: 未找到torrent文件")
        sys.exit(1)

    print(f"\n找到 {len(file_paths)} 个torrent文件\n")

    # 处理每个文件
    magnets = []
    for i, torrent_path in enumerate(file_paths, 1):
        print(f"\n[{i}/{len(file_paths)}]", end=" ")
        converter = TorrentToMagnet(torrent_path)
        magnet = converter.convert()

        if magnet:
            magnets.append(magnet)
            print("\n" + "=" * 60)
            print("Magnet链接:")
            print(magnet)
            print("=" * 60)
        else:
            print(f"\n失败: 无法转换 {torrent_path}")

    # 结果汇总
    print(f"\n\n转换完成! 成功: {len(magnets)}/{len(file_paths)}")

    # 如果只有一个magnet，尝试复制到剪贴板
    if len(magnets) == 1:
        copy_to_clipboard(magnets[0])
    elif magnets:
        print("\n提示: 批量转换完成，请查看上面的magnet链接")

    # 保持窗口打开（仅Windows双击运行时）
    if sys.stdout.isatty() and os.name == 'nt':
        input("\n按回车键退出...")


if __name__ == '__main__':
    main()