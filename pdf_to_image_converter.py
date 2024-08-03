import os
import time
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf2image import convert_from_path

class PDFHandler(FileSystemEventHandler):
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            print(f"檢測到新的PDF文件: {event.src_path}")
            pdf_to_images(event.src_path, self.output_folder)

def pdf_to_images(pdf_path, output_folder):
    # 創建以PDF文件名命名的子文件夾
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    os.makedirs(pdf_output_folder, exist_ok=True)
    
    # 轉換 PDF 到高品質圖像
    images = convert_from_path(pdf_path, dpi=300, fmt='png')
    
    # 保存高品質圖像
    for i, image in enumerate(images):
        image_path = os.path.join(pdf_output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG", quality=100)
        print(f"已保存 {pdf_name} 的第 {i + 1} 頁為高品質圖像: {image_path}")

def select_folder(prompt):
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    folder_path = filedialog.askdirectory(title=prompt)
    return folder_path

# 主程序
if __name__ == "__main__":
    print("請選擇輸入文件夾（放置PDF文件的文件夾）：")
    input_folder = select_folder("選擇輸入文件夾")
    if not input_folder:
        print("未選擇輸入文件夾，程序退出。")
        exit()
    
    print("請選擇輸出文件夾（保存圖像的文件夾）：")
    output_folder = select_folder("選擇輸出文件夾")
    if not output_folder:
        print("未選擇輸出文件夾，程序退出。")
        exit()
    
    print(f"監視的輸入文件夾: {input_folder}")
    print(f"圖像輸出文件夾: {output_folder}")
    
    event_handler = PDFHandler(input_folder, output_folder)
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    print("開始監視文件夾，按 Ctrl+C 退出程序...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
