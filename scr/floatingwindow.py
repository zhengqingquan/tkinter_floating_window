"""
tkinter
"""
import tkinter as tk
import win32gui, win32api
import os, sys
import win32con
import pywintypes
import threading
import time


class FloatingWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # 建立一个没有任何按钮，无法关闭，最大化，最小化的窗口。该方法必须放在init_parent_window()之前，否则会被显示桌面隐藏。
        self.wm_attributes("-toolwindow", True)  # 置为工具窗口（右上角只有关闭按钮）。该方法必须放在init_parent_window()之前，否则会被显示桌面隐藏。
        self.update()  # 初始化后刷新窗口数据，否则只有tkinter的初始值。这样会导致找不到顶级窗口句柄。
        self.init_parent_window()  # 设置父窗口为桌面。
        self.init_style()  # 设置窗口风格。
        self.init_event()  # 设置窗口事件。

        # self.self_handle = self.frame() # 十六进制的句柄（类名是TkChild）
        # self.self_handle = self.winfo_id() # 十进制的句柄（类名是TkChild）

    def init_parent_window(self):
        # 获得桌面的句柄
        Progman_handle = win32gui.FindWindow("Progman", None)
        # GW_HWNDFIRST = 0  # 同级别第一个窗口
        # GW_HWNDLAST = 1  # 同级别最后一个窗口
        # GW_HWNDNEXT = 2  # 同级别下一个窗口
        # GW_HWNDPREV = 3  # 同级别上一个窗口
        # GW_OWNER = 4  # 属主窗口
        GW_CHILD = 5  # 子窗口
        # GW_ENABLEDPOPUP = 6  # enabled popup window有效的弹出窗口
        SHELLDLL_DefView_handle = win32gui.GetWindow(Progman_handle, 5)
        SysListView32_handle = win32gui.GetWindow(SHELLDLL_DefView_handle, GW_CHILD)
        print(f"桌面的句柄为：{SysListView32_handle}")

        # 获得顶级窗口的句柄
        tk_top = win32gui.FindWindow("TkTopLevel", self.title())
        print(f"TkTopLevel的句柄为：{tk_top}")

        # 设置父窗口为桌面
        win32gui.SetParent(tk_top, SysListView32_handle)

    def init_style(self):
        width = None
        height = None
        self.width, self.height = width, height
        self.maxsize(600, 400)  # 最大600x400
        self["bg"] = "gray"  # 背景设为灰色
        self.wm_attributes("-alpha", 0.4)  # 透明度。更改透明度必须放init_parent_window()后面，否则窗口会消失。

    def init_event(self):
        self.bind('<B1-Motion>', self._on_move)  # 拖动左键
        self.bind('<ButtonPress-1>', self._on_tap)  # 单击左键

    # def set_display_postion(self, offset_x, offset_y):
    #     self.geometry("+%s+%s" % (offset_x, offset_y))
    #
    # def set_window_size(self, w, h):
    #     self.width, self.height = w, h
    #     self.geometry("%sx%s" % (w, h))

    def _on_move(self, event):
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (self.width, self.height,
                                       self.abs_x + offset_x, self.abs_y + offset_y)
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y = event.x_root, event.y_root
        self.abs_x, self.abs_y = self.winfo_x(), self.winfo_y()

if __name__ == '__main__':
    fw = FloatingWindow()
    fw.mainloop()
