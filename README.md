# tkinter_floating_window
A Tkinter window that will not be killed by the display desktop

这是一个tkinter的悬浮窗口，并且不会被win10的显示桌面给隐藏掉。甚至还可以自由拖动窗口位置。
缺点是无法将窗口置为顶层（用于显示在最前面）。或许在之后可以找到方法修改。

# demo pictures
![image](https://github.com/zhengqingquan/gallery/blob/main/tkinter_floating_window/Video_2021-06-10_171212.gif?raw=true)   

# library & Train of thought
这里使用了win32gui的库。
通过将tkinter的父窗口设置为桌面，来达到预定效果。

# change
1.1.0 修改错误：当你曾创建过虚拟桌面时，将无法创建悬浮窗口。
1.0.0 初版：可以在window10的桌面创建悬浮窗口，并且不受“显示桌面”功能的影响。