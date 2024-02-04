import re

def contains_chinese(line):
    """
    检查给定的行是否包含中文字符。
    
    参数:
    - line: 字符串，待检查的文本行。
    
    返回:
    - 布尔值，如果行包含中文字符，则为True；否则为False。
    """
    return re.search("[\u4e00-\u9fff]", line) is not None

def process_subtitle_text(text):
    """
    处理字幕文本，将连续的英文行和中文行合并为一行，并按照“序号、时间戳、英文、中文”的格式进行整理。
    
    参数:
    - text: 字符串，包含原始的字幕文本，预期包含序号、时间戳、英文和中文行。
    
    返回:
    - final_text: 字符串，处理后的字幕文本。
    """
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
        elif contains_chinese(line):  # 检查是否包含中文
            chinese_lines.append(line)
        else:  # 默认为英文行
            english_lines.append(line)

    append_processed_segment()
    final_text = "\n\n".join(processed_text)
    return final_text

def process_subtitle_file(input_file_path, output_file_path):
    """
    从指定的输入文件读取字幕文本，处理后输出到指定的输出文件。
    
    参数:
    - input_file_path: 字符串，输入文件的路径。
    - output_file_path: 字符串，输出文件的路径。
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            original_text = file.read()

        processed_text = process_subtitle_text(original_text)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)

        print("处理成功，输出文件已保存。")
    except Exception as e:
        print(f"处理失败: {str(e)}")

if __name__ == "__main__":
    input_file_path = input("输入文件路径（.txt）：")
    output_file_path = input("输出文件路径（.txt）：")

    process_subtitle_file(input_file_path, output_file_path)
    print("处理结束！")
