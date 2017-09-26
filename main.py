# -*- coding: utf-8 -*-

try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2

from controller.controller import Controller


def main():
    root = tk.Tk()
    root.title("Latch'sApp")
    # root.iconbitmap('img/icon.icns')
    root.resizable(0, 0)
    app = Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main() 
