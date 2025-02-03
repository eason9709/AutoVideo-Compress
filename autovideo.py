import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from moviepy.editor import VideoFileClip
import threading
import sys
import tempfile
from moviepy.config import change_settings

def get_ffmpeg_path():
    """
    使用相對路徑取得 ffmpeg 執行檔。
    預設結構：
      vid/
        imageio_ffmpeg/
          binaries/
            ffmpeg-win-x86_64-v7.1.exe
        autovideo.py
    若該路徑不存在，再嘗試在同一目錄尋找 ffmpeg.exe。
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_path = os.path.join(base_path, "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
        print(f"使用相對路徑設定 FFMPEG 路徑: {ffmpeg_path}")

        if not os.path.exists(ffmpeg_path):
            print(f"{ffmpeg_path} 不存在, 嘗試在同一目錄尋找 ffmpeg.exe")
            ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
            if not os.path.exists(ffmpeg_path):
                print("找不到 ffmpeg！")
                return None
        print(f"最終使用的 FFMPEG 路徑: {ffmpeg_path}")
        return ffmpeg_path
    except Exception as e:
        print(f"獲取 FFMPEG 路徑錯誤: {str(e)}")
        return None

# 在程式啟動時設置 ffmpeg 路徑
ffmpeg_path = get_ffmpeg_path()
if ffmpeg_path:
    print(f"設置 FFMPEG 路徑: {ffmpeg_path}")
    change_settings({"FFMPEG_BINARY": ffmpeg_path})
else:
    print("無法設置 FFMPEG 路徑")

class VideoCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("影片壓縮工具")
        self.root.geometry("600x700")
        
        # 主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 檔案選擇區域
        file_frame = ttk.LabelFrame(main_frame, text="影片檔案選擇", padding="5")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 檔案列表
        self.file_listbox = tk.Listbox(file_frame, height=10)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 檔案操作按鈕
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="添加檔案", command=self.add_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清除所有", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="移除選中", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        
        # 設定區域
        settings_frame = ttk.LabelFrame(main_frame, text="設定", padding="5")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 輸出資料夾
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(output_frame, text="輸出資料夾:").pack(side=tk.LEFT)
        self.output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="瀏覽", command=self.browse_output).pack(side=tk.LEFT)
        
        # 目標檔案大小設定
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(size_frame, text="目標大小 (MB):").pack(side=tk.LEFT)
        self.target_size = tk.IntVar(value=10)
        ttk.Entry(size_frame, textvariable=self.target_size, width=10).pack(side=tk.LEFT, padx=5)
        
        # 狀態顯示
        self.status_text = tk.Text(main_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 開始按鈕
        self.start_button = ttk.Button(main_frame, text="開始轉換", command=self.start_conversion)
        self.start_button.pack(pady=10)
        
        # 儲存檔案路徑
        self.video_files = []

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="選擇影片檔案",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.video_files:
                self.video_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.video_files.clear()
    
    def remove_selected(self):
        selection = self.file_listbox.curselection()
        for index in reversed(selection):
            self.file_listbox.delete(index)
            self.video_files.pop(index)
    
    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
    
    def compress_video(self, input_path, output_path):
        temp_output = None
        try:
            target_size = self.target_size.get() * 1024 * 1024  # 轉換為位元組
            
            # 修正路徑格式，使用 os.path 來處理路徑
            output_path = os.path.normpath(output_path)
            output_dir = os.path.dirname(output_path)
            filename = os.path.splitext(os.path.basename(output_path))[0]
            temp_output = os.path.join(output_dir, f"{filename}_temp.mp4")
            
            # 確保輸入檔案存在
            if not os.path.exists(input_path):
                raise Exception("找不到輸入檔案")
            
            # 確保輸出路徑可寫入
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 載入影片
            clip = VideoFileClip(input_path)
            if clip is None:
                raise Exception("無法載入影片檔案")
            
            # 獲取原始檔案資訊
            original_width = clip.w
            original_height = clip.h
            original_aspect_ratio = original_width / original_height
            original_size = os.path.getsize(input_path)
            original_bitrate = original_size * 8 / clip.duration
            duration = clip.duration
            
            # 計算目標比特率（預留10%空間以確保達到目標大小）
            target_total_bitrate = (target_size * 8) / duration * 0.9
            compression_ratio = target_size / original_size
            
            # 分配比特率（固定音頻佔5%）
            target_audio_bitrate = target_total_bitrate * 0.05
            target_video_bitrate = target_total_bitrate * 0.95
            
            # 顯示詳細資訊
            self.update_status(f"原始檔案大小: {original_size / (1024*1024):.2f}MB")
            self.update_status(f"原始比特率: {int(original_bitrate/1000)}kbps")
            self.update_status(f"目標總比特率: {int(target_total_bitrate/1000)}kbps")
            self.update_status(f"目標視頻比特率: {int(target_video_bitrate/1000)}kbps")
            self.update_status(f"目標音頻比特率: {int(target_audio_bitrate/1000)}kbps")
            self.update_status(f"壓縮比例: {compression_ratio:.2%}")
            
            # 定義可能的分辨率等級（高度）
            resolutions = [1080, 720, 576, 480, 360, 240]
            
            # 根據壓縮比例選擇起始分辨率
            if compression_ratio < 0.1:
                start_index = resolutions.index(480)  # 從480p開始
            elif compression_ratio < 0.3:
                start_index = resolutions.index(720)  # 從720p開始
            else:
                start_index = 0  # 從1080p開始
            
            resolutions = resolutions[start_index:]
            
            # 嘗試不同的分辨率直到達到目標大小
            for height in resolutions:
                # 計算對應的寬度（保持比例）
                if original_height > original_width:  # 直向影片
                    new_height = min(height, original_height)
                    new_width = int(new_height * original_aspect_ratio)
                    new_width = new_width - (new_width % 2)
                    new_height = int(new_width / original_aspect_ratio)
                    new_height = new_height - (new_height % 2)
                else:  # 橫向影片
                    new_width = min(int(height * original_aspect_ratio), original_width)
                    new_height = int(new_width / original_aspect_ratio)
                    new_height = new_height - (new_height % 2)
                    new_width = int(new_height * original_aspect_ratio)
                    new_width = new_width - (new_width % 2)
                
                try:
                    self.update_status(f"嘗試分辨率: {new_width}x{new_height}")
                    self.update_status(f"視頻比特率: {int(target_video_bitrate/1000)}kbps")
                    self.update_status(f"音頻比特率: {int(target_audio_bitrate/1000)}kbps")
                    
                    # 調整影片尺寸和幀率
                    resized_clip = clip.resize((new_width, new_height))  # 使用元組方式傳入尺寸
                    if clip.fps > 30:
                        resized_clip = resized_clip.set_fps(30)
                    
                    # 寫入檔案前確保目錄存在
                    temp_dir = os.path.dirname(temp_output)
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    
                    # 寫入檔案
                    try:
                        resized_clip.write_videofile(
                            temp_output,
                            bitrate=f"{int(target_video_bitrate/1000)}k",
                            audio_bitrate=f"{int(target_audio_bitrate/1000)}k",
                            codec='libx264',
                            audio_codec='aac',
                            preset='medium',
                            threads=4,
                            fps=min(clip.fps, 30),
                            ffmpeg_params=[
                                '-profile:v', 'main',
                                '-level', '4.0',
                                '-pix_fmt', 'yuv420p'
                            ]
                        )
                    except Exception as e:
                        self.update_status(f"寫入檔案時發生錯誤: {str(e)}")
                        self.update_status(f"resized_clip: {resized_clip}")
                        self.update_status(f"temp_output: {temp_output}")
                        if temp_output and os.path.exists(temp_output):
                            os.remove(temp_output)
                        raise
                    
                    # 檢查輸出檔案大小
                    if os.path.exists(temp_output):
                        output_size = os.path.getsize(temp_output)
                        self.update_status(f"當前檔案大小: {output_size / (1024 * 1024):.2f} MB")
                        
                        if output_size <= target_size:
                            if os.path.exists(output_path):
                                os.remove(output_path)
                            os.rename(temp_output, output_path)
                            self.update_status(f"成功壓縮到目標大小，最終分辨率: {new_width}x{new_height}")
                            break
                        else:
                            if os.path.exists(temp_output):
                                os.remove(temp_output)
                    else:
                        raise Exception("無法創建輸出檔案")
                    
                except Exception as e:
                    self.update_status(f"處理當前分辨率時發生錯誤: {str(e)}")
                    if temp_output and os.path.exists(temp_output):
                        os.remove(temp_output)
                    continue
            
            clip.close()
        except Exception as e:
            self.update_status(f"處理錯誤: {str(e)}")
            if temp_output and os.path.exists(temp_output):
                os.remove(temp_output)

    def process_files(self):
        output_folder = self.output_path.get()
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        total_files = len(self.video_files)
        if total_files == 0:
            self.update_status("請選擇要轉換的影片檔案！")
            return
        
        self.update_status(f"開始處理 {total_files} 個檔案")
        
        for i, input_path in enumerate(self.video_files):
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_folder, f"compressed_{filename}")
            
            self.update_status(f"\n處理檔案: {filename}")
            try:
                self.compress_video(input_path, output_path)
                self.update_status(f"檔案 {filename} 轉換完成")
            except Exception as e:
                self.update_status(f"處理檔案 {filename} 時發生錯誤: {str(e)}")
        
        self.update_status("\n所有檔案處理完成！")
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("完成", "影片轉換完成！")
    
    def start_conversion(self):
        if not self.video_files:
            messagebox.showerror("錯誤", "請選擇要轉換的影片檔案！")
            return
        
        if not self.output_path.get():
            messagebox.showerror("錯誤", "請選擇輸出資料夾！")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.status_text.delete(1.0, tk.END)
        
        threading.Thread(target=self.process_files, daemon=True).start()

def main():
    root = tk.Tk()
    app = VideoCompressorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()