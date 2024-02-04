import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def contains_chinese(line):
    import re
    return re.search("[\u4e00-\u9fff]", line) is not None

def process_subtitle_text(text):
    lines = text.strip().split("\n")
    processed_text = []
    index, timestamp = '', ''
    english_lines, chinese_lines = [], []

    def append_processed_segment():
        nonlocal processed_text, index, timestamp, english_lines, chinese_lines
        if index and timestamp and (english_lines or chinese_lines):
            english_text = " ".join(english_lines)
            chinese_text = "".join(chinese_lines)
            processed_segment = f"{index}\n{timestamp}\n{english_text}\n{chinese_text}"
            processed_text.append(processed_segment)
        english_lines, chinese_lines = [], []

    for line in lines:
        if line.isdigit():
            append_processed_segment()
            index = line
        elif "-->" in line:
            timestamp = line
        elif contains_chinese(line):
            chinese_lines.append(line)
        else:
            english_lines.append(line)

    append_processed_segment()
    final_text = "\n\n".join(processed_text)
    return final_text

def process_file():
    input_file_path = filedialog.askopenfilename(title="选择输入文件", filetypes=[("Text files", "*.txt")])
    output_file_path = filedialog.asksaveasfilename(title="保存输出文件", filetypes=[("Text files", "*.txt")])

    if input_file_path and output_file_path:
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                original_text = file.read()
            processed_text = process_subtitle_text(original_text)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(processed_text)
            messagebox.showinfo("成功", "处理成功，输出文件已保存。")
        except Exception as e:
            messagebox.showerror("错误", f"处理失败: {str(e)}")

def create_gui():
    root = tk.Tk()
    root.title("字幕处理工具")

    tk.Label(root, text="欢迎使用字幕处理工具", font=("Arial", 12)).pack(pady=20)

    tk.Button(root, text="选择文件并处理", command=process_file).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
