"""
FloatingWindow
windows10的悬浮窗口。可以不受windows10任务栏的“显示桌面”功能影响。
"""
import tkinter as tk
import win32gui


class FloatingWindow(tk.Tk):
    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0
    width, height = None, None

    def __init__(self):
        super().__init__()  # 先进行tk.Tk的初始化
        self.SysListView32_handle = 0  # 保存SysListView32窗口的句柄
        self.overrideredirect(True)  # 建立一个没有任何按钮，无法关闭，最大化，最小化的窗口。该方法必须放在init_parent_window()之前，否则会被显示桌面隐藏。
        self.wm_attributes("-toolwindow", True)  # 置为工具窗口（右上角只有关闭按钮）。该方法必须放在init_parent_window()之前，否则会被显示桌面隐藏。
        self.update()  # 初始化后刷新窗口数据，否则只有tkinter的初始值。这样会导致找不到顶级窗口句柄。
        self.init_parent_window()  # 设置父窗口为桌面。
        self.init_style()  # 设置窗口风格。
        self.init_event()  # 设置窗口事件。

        # self.self_handle = self.frame() # 十六进制的句柄（类名是TkChild）
        # self.self_handle = self.winfo_id() # 十进制的句柄（类名是TkChild）

    def init_parent_window(self):
        # 使用枚举遍历获取SysListView32的句柄。
        win32gui.EnumWindows(self.find_SysListView32, 0)
        print(f"SysListView32_handle的句柄为：{self.SysListView32_handle}")

        # 获得自身顶级窗口的句柄
        tk_top = win32gui.FindWindow("TkTopLevel", self.title())
        print(self.title())
        print(f"TkTopLevel的句柄为：{tk_top}")

        # 设置父窗口为桌面
        win32gui.SetParent(tk_top, self.SysListView32_handle)

    def find_SysListView32(self, hwnd, mouse):
        """
        用来查找桌面SysListView32的回调函数。
        :param hwnd:窗口的句柄
        :param mouse:回调函数的参数，该值为0。
        :return:None
        """
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(
                hwnd) and win32gui.GetWindow(hwnd, 5):  # 窗口存在，且窗口可用，且窗口看得见，且窗口有子窗口。
            if win32gui.GetClassName(win32gui.GetWindow(hwnd, 5)) == 'SHELLDLL_DefView':
                # print(win32gui.GetClassName(win32gui.GetWindow(win32gui.GetWindow(hwnd, 5), 5)))
                # print(win32gui.GetWindow(win32gui.GetWindow(hwnd, 5), 5))
                self.SysListView32_handle = win32gui.GetWindow(win32gui.GetWindow(hwnd, 5), 5)

    def init_style(self):
        """
        用来初始化窗口的风格（样式）
        :return:None
        """
        self.maxsize(600, 400)  # 最大600x400
        self["bg"] = "gray"  # 背景设为灰色
        self.wm_attributes("-alpha", 0.4)  # 透明度。更改透明度必须放init_parent_window()后面，否则窗口会消失。

    def init_event(self):
        """
        用来添加窗口的事件
        :return:None
        """
        self.bind('<B1-Motion>', self._on_move)  # 左键拖动
        self.bind('<ButtonPress-1>', self._on_tap)  # 单击左键

    # def set_display_postion(self, offset_x, offset_y):
    #     self.geometry("+%s+%s" % (offset_x, offset_y))
    #
    # def set_window_size(self, w, h):
    #     self.width, self.height = w, h
    #     self.geometry("%sx%s" % (w, h))

    def _on_move(self, event):
        """
        左键拖动事件
        :param event:事件参数
        :return:
        """
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (self.width, self.height,
                                       self.abs_x + offset_x, self.abs_y + offset_y)
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        """
        单击左键事件
        :param event: 事件参数
        :return:
        """
        self.root_x, self.root_y = event.x_root, event.y_root
        self.abs_x, self.abs_y = self.winfo_x(), self.winfo_y()


if __name__ == '__main__':
    fw = FloatingWindow()
    fw.mainloop()
