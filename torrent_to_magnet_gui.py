#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Torrent种子文件转Magnet磁力链接工具 - GUI版本
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import sys
import hashlib
import bencodepy
from urllib.parse import quote
import tkinterdnd2 as tkdnd


class TorrentToMagnetGUI:
    """Torrent转Magnet转换器 - GUI版本"""

    def __init__(self, root):
        self.root = root
        self.root.title("Torrent转Magnet工具 v20260523.1207")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 设置主题样式
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 设置颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a90d9"
        self.hover_color = "#5aa0e9"

        self.root.configure(bg=self.bg_color)

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        title_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            title_frame,
            text="🧲 Torrent转Magnet工具",
            font=("Microsoft YaHei UI", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 5))

        subtitle_label = ttk.Label(
            title_frame,
            text="拖拽torrent文件到下方区域，或点击浏览按钮选择文件",
            font=("Microsoft YaHei UI", 9),
            foreground="#666666"
        )
        subtitle_label.grid(row=1, column=0)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)

        # 拖拽区域
        self.drop_frame = tk.Frame(file_frame, height=150, bg="#e8e8e8", relief="ridge", borderwidth=2)
        self.drop_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.rowconfigure(0, weight=0)
        file_frame.rowconfigure(1, weight=0)

        self.drop_label = tk.Label(
            self.drop_frame,
            text="📁 将torrent文件拖拽到此处\n或点击右侧按钮选择文件",
            bg="#e8e8e8",
            font=("Microsoft YaHei UI", 10),
            justify=tk.CENTER
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 注册拖拽事件
        self.drop_frame.drop_target_register(tkdnd.DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)

        # 文件列表
        files_frame = ttk.Frame(file_frame)
        files_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.rowconfigure(1, weight=1)
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)

        # 文件列表带滚动条
        list_scroll = ttk.Scrollbar(files_frame)
        list_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.file_listbox = tk.Listbox(
            files_frame,
            height=8,
            yscrollcommand=list_scroll.set,
            font=("Microsoft YaHei UI", 9)
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_scroll.config(command=self.file_listbox.yview)

        # 按钮区域
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        self.browse_button = ttk.Button(
            button_frame,
            text="📂 浏览文件",
            command=self.browse_files,
            width=15
        )
        self.browse_button.grid(row=0, column=0, padx=(0, 5))

        self.clear_button = ttk.Button(
            button_frame,
            text="🗑️ 清除列表",
            command=self.clear_files,
            width=15
        )
        self.clear_button.grid(row=0, column=1, padx=(0, 5))

        self.convert_button = ttk.Button(
            button_frame,
            text="🔄 开始转换",
            command=self.convert_files,
            width=15,
            style="Accent.TButton"
        )
        self.convert_button.grid(row=0, column=2)

        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="转换结果", padding="10")
        result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=15,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 9),
            state=tk.DISABLED
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置文本标签
        self.result_text.tag_config("title", font=("Microsoft YaHei UI", 11, "bold"), foreground="#4a90d9")
        self.result_text.tag_config("success", foreground="#28a745")
        self.result_text.tag_config("error", foreground="#dc3545")
        self.result_text.tag_config("info", foreground="#666666")
        self.result_text.tag_config("magnet", font=("Microsoft YaHei UI", 8), foreground="#6c757d", background="#f8f9fa")

        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))

        self.copy_button = ttk.Button(
            bottom_frame,
            text="📋 复制结果",
            command=self.copy_result,
            width=20
        )
        self.copy_button.grid(row=0, column=0, padx=(0, 10))

        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Microsoft YaHei UI", 8)
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def on_drag_enter(self, event):
        """拖拽进入事件"""
        self.drop_frame.config(bg="#d0e8ff")
        self.drop_label.config(bg="#d0e8ff")

    def on_drag_leave(self, event):
        """拖拽离开事件"""
        self.drop_frame.config(bg="#e8e8e8")
        self.drop_label.config(bg="#e8e8e8")

    def on_drop(self, event):
        """拖拽放下事件"""
        self.drop_frame.config(bg="#e8e8e8")
        self.drop_label.config(bg="#e8e8e8")

        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            file_path = file_path.strip('{}')  # 移除可能的大括号
            if os.path.isfile(file_path) and file_path.lower().endswith('.torrent'):
                self.add_file(file_path)
            elif os.path.isdir(file_path):
                # 如果是目录，搜索其中的torrent文件
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        if file.lower().endswith('.torrent'):
                            self.add_file(os.path.join(root, file))

    def browse_files(self):
        """浏览文件对话框"""
        files = filedialog.askopenfilenames(
            title="选择Torrent文件",
            filetypes=[("Torrent files", "*.torrent"), ("All files", "*.*")]
        )
        for file_path in files:
            self.add_file(file_path)

    def add_file(self, file_path):
        """添加文件到列表"""
        if file_path not in self.file_listbox.get(0, tk.END):
            self.file_listbox.insert(tk.END, file_path)
            self.status_var.set(f"已添加: {os.path.basename(file_path)}")

    def clear_files(self):
        """清除文件列表"""
        self.file_listbox.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.status_var.set("列表已清除")

    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def convert_torrent(self, torrent_path):
        """转换单个torrent文件"""
        try:
            with open(torrent_path, 'rb') as f:
                torrent_data = bencodepy.decode(f.read())
        except Exception as e:
            return None, f"无法加载文件: {e}"

        try:
            info = torrent_data.get(b'info')
            if not info:
                return None, "文件缺少info字段"

            encoded_info = bencodepy.encode(info)
            sha1 = hashlib.sha1(encoded_info)
            info_hash = sha1.hexdigest()

            # 提取名称
            name = info.get(b'name', b'Unknown')
            name = name.decode('utf-8', errors='ignore')

            # 提取tracker
            trackers = []
            announce = torrent_data.get(b'announce')
            if announce:
                trackers.append(announce.decode('utf-8', errors='ignore'))

            announce_list = torrent_data.get(b'announce-list')
            if announce_list:
                for tracker_list in announce_list:
                    for tracker in tracker_list:
                        tracker_str = tracker.decode('utf-8', errors='ignore')
                        if tracker_str not in trackers:
                            trackers.append(tracker_str)

            # 计算总大小
            total_size = 0
            if b'length' in info:
                total_size = info.get(b'length', 0)
            elif b'files' in info:
                for file_info in info.get(b'files', []):
                    total_size += file_info.get(b'length', 0)

            # 生成magnet链接
            magnet_parts = [f"magnet:?xt=urn:btih:{info_hash}"]
            magnet_parts.append(f"&dn={quote(name)}")

            for tracker in trackers[:5]:
                magnet_parts.append(f"&tr={quote(tracker)}")

            if total_size > 0:
                magnet_parts.append(f"&xl={total_size}")

            magnet = ''.join(magnet_parts)

            result = {
                'name': name,
                'size': self.format_size(total_size),
                'info_hash': info_hash,
                'tracker_count': len(trackers),
                'magnet': magnet
            }

            return result, None

        except Exception as e:
            return None, f"转换失败: {e}"

    def convert_files(self):
        """转换所有文件"""
        files = self.file_listbox.get(0, tk.END)
        if not files:
            messagebox.showwarning("警告", "请先添加torrent文件")
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        success_count = 0
        for i, file_path in enumerate(files, 1):
            self.status_var.set(f"正在转换 ({i}/{len(files)}): {os.path.basename(file_path)}")
            self.root.update()

            result, error = self.convert_torrent(file_path)

            if result:
                success_count += 1
                self.result_text.insert(tk.END, f"\n{'='*70}\n", "title")
                self.result_text.insert(tk.END, f"✓ {os.path.basename(file_path)}\n", "success")
                self.result_text.insert(tk.END, f"{'='*70}\n\n", "title")
                self.result_text.insert(tk.END, f"文件名: {result['name']}\n", "info")
                self.result_text.insert(tk.END, f"大小: {result['size']}\n", "info")
                self.result_text.insert(tk.END, f"Info Hash: {result['info_hash']}\n", "info")
                self.result_text.insert(tk.END, f"Tracker数量: {result['tracker_count']}\n", "info")
                self.result_text.insert(tk.END, f"\nMagnet链接:\n", "title")
                self.result_text.insert(tk.END, f"{result['magnet']}\n", "magnet")
            else:
                self.result_text.insert(tk.END, f"\n✗ {os.path.basename(file_path)}\n", "error")
                self.result_text.insert(tk.END, f"错误: {error}\n", "error")

        self.result_text.config(state=tk.DISABLED)
        self.status_var.set(f"转换完成! 成功: {success_count}/{len(files)}")

    def copy_result(self):
        """复制结果到剪贴板"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("提示", "没有可复制的内容")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("成功", "结果已复制到剪贴板")

    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """主函数"""
    # 创建根窗口并启用拖拽支持
    root = tkdnd.TkinterDnD.Tk()

    # 创建应用
    app = TorrentToMagnetGUI(root)

    # 运行应用
    app.run()


if __name__ == '__main__':
    main()
