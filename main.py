import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time

def merge_bin_files(file_a_path, addr_a, file_b_path, addr_b, output_path):
    with open(file_a_path, 'rb') as fa:
        data_a = fa.read()
    with open(file_b_path, 'rb') as fb:
        data_b = fb.read()

    if addr_a <= addr_b:
        first_addr, first_data = addr_a, data_a
        second_addr, second_data = addr_b, data_b
    else:
        first_addr, first_data = addr_b, data_b
        second_addr, second_data = addr_a, data_a

    end_first = first_addr + len(first_data)
    start_second = second_addr
    end_second = second_addr + len(second_data)

    total_size = max(end_first, end_second)
    merged = bytearray([0xFF] * (total_size - min(first_addr, second_addr)))

    offset_first = first_addr - min(first_addr, second_addr)
    merged[offset_first:offset_first+len(first_data)] = first_data

    offset_second = second_addr - min(first_addr, second_addr)
    merged[offset_second:offset_second+len(second_data)] = second_data

    with open(output_path, 'wb') as fout:
        fout.write(merged)

def select_file(entry_widget):
    file_path = filedialog.askopenfilename(title="选择BIN文件", filetypes=[("BIN Files", "*.bin")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def select_output_file(entry_widget):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    default_name = f"BMS_BIN_{timestamp}.bin"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".bin",
        title="保存合并后的BIN文件",
        initialfile=default_name,
        filetypes=[("BIN Files", "*.bin")]
    )
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def start_merge():
    try:
        file_a = entry_bootloader.get()
        addr_a = int(entry_addr_bootloader.get(), 16)
        file_b = entry_application.get()
        addr_b = int(entry_addr_application.get(), 16)
        output_file = entry_output.get()

        if not os.path.isfile(file_a) or not os.path.isfile(file_b):
            messagebox.showerror("错误", "请选择正确的Bootloader或Application文件！")
            return

        if not output_file:
            messagebox.showerror("错误", "请选择输出文件路径！")
            return

        merge_bin_files(file_a, addr_a, file_b, addr_b, output_file)
        messagebox.showinfo("成功", f"合并成功！文件已保存到:\n{output_file}")

    except Exception as e:
        messagebox.showerror("异常", f"出现错误: {str(e)}")

def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(size)

# 创建主窗口
root = tk.Tk()
root.title("BIN文件合并工具")
center_window(root, 600, 400)
root.configure(bg="#ffffff")
root.resizable(False, False)

font_title = ("Helvetica", 16, "bold")
font_label = ("Helvetica", 11)
font_entry = ("Helvetica", 10)

# 标题
tk.Label(root, text="BIN 文件合并工具", bg="#ffffff", fg="#333333", font=font_title).pack(pady=20)

frame = tk.Frame(root, bg="#ffffff")
frame.pack(pady=10)

# Bootloader
tk.Label(frame, text="Bootloader路径:", bg="#ffffff", font=font_label).grid(row=0, column=0, sticky='e', padx=10, pady=8)
entry_bootloader = tk.Entry(frame, width=45, font=font_entry)
entry_bootloader.grid(row=0, column=1, padx=5)
tk.Button(frame, text="选择文件", command=lambda: select_file(entry_bootloader), bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

tk.Label(frame, text="Bootloader地址:", bg="#ffffff", font=font_label).grid(row=1, column=0, sticky='e', padx=10, pady=8)
entry_addr_bootloader = tk.Entry(frame, width=45, font=font_entry)
entry_addr_bootloader.grid(row=1, column=1, padx=5)
entry_addr_bootloader.insert(0, "0x08000000")

# Application
tk.Label(frame, text="Application路径:", bg="#ffffff", font=font_label).grid(row=2, column=0, sticky='e', padx=10, pady=8)
entry_application = tk.Entry(frame, width=45, font=font_entry)
entry_application.grid(row=2, column=1, padx=5)
tk.Button(frame, text="选择文件", command=lambda: select_file(entry_application), bg="#4CAF50", fg="white").grid(row=2, column=2, padx=5)

tk.Label(frame, text="Application地址:", bg="#ffffff", font=font_label).grid(row=3, column=0, sticky='e', padx=10, pady=8)
entry_addr_application = tk.Entry(frame, width=45, font=font_entry)
entry_addr_application.grid(row=3, column=1, padx=5)
entry_addr_application.insert(0, "0x08020000")

# 输出文件
tk.Label(frame, text="输出文件路径:", bg="#ffffff", font=font_label).grid(row=4, column=0, sticky='e', padx=10, pady=8)
entry_output = tk.Entry(frame, width=45, font=font_entry)
entry_output.grid(row=4, column=1, padx=5)
tk.Button(frame, text="保存为", command=lambda: select_output_file(entry_output), bg="#2196F3", fg="white").grid(row=4, column=2, padx=5)

# 合并按钮
tk.Button(root, text="开始合并", command=start_merge, width=25, height=2, bg="#FF5722", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

# 启动主循环
root.mainloop()
