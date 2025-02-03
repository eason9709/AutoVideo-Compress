# 影片壓縮工具

## 簡介
這個工具是一款使用 Python 撰寫的影片壓縮程式，提供簡單易用的圖形介面（基於 Tkinter），讓您即使不熟悉 Python 也能輕鬆壓縮影片。  
程式利用 MoviePy 處理影片，並透過 pip 安裝的 **imageio-ffmpeg** 自動取得與管理 ffmpeg 執行檔，無需您手動下載或提供大型檔案。

**主要功能：**
- 批次壓縮多個影片檔案
- 自訂目標檔案大小（MB）
- 自動調整解析度與壓縮參數
- 進度與錯誤訊息即時顯示

---

## 環境需求
- **作業系統：** Windows、macOS 或 Linux
- **Python版本：** Python 3.6 以上版本
- **必要套件：**
  - moviepy
  - Pillow
  - imageio-ffmpeg
- **Tkinter：** 隨 Python 內建（通常不需另行安裝）

---

## 安裝步驟

### 1. 安裝 Python
若您的電腦尚未安裝 Python，請依照下列步驟操作：
1. 前往官方網站下載：[Python 官網](https://www.python.org/downloads/)  
   建議下載最新版本的 Python 3.x。
2. 執行安裝程式，**務必選取「Add Python to PATH」** 選項，這樣您便可以在命令提示字元中直接使用 Python。

### 2. 下載專案程式碼
1. 前往 GitHub 或其他來源下載本專案的原始程式碼（通常提供壓縮檔）。
2. 將壓縮檔解壓縮到您所選擇的資料夾中，例如：`C:\Users\您的名字\Downloads\VideoCompressor\`

### 3. 安裝必要 Python 套件
1. 開啟命令提示字元 (Command Prompt) 或 PowerShell：
   - Windows 使用者可以按 `Win + R`，輸入 `cmd` 或 `powershell`，然後按 Enter。
2. 使用 `cd` 命令切換到您剛解壓縮的專案資料夾。例如：
   ```powershell
   cd C:\Users\您的名字\Downloads\VideoCompressor
   ```
3. 確認該資料夾中有以下檔案：
   - `autovideo.py`
   - `requirements.txt`
4. 執行以下指令以安裝所有必要套件：
   ```powershell
   pip install -r requirements.txt
   ```
   此步驟會自動從網路上下載並安裝 moviepy、Pillow 及 imageio-ffmpeg 等套件。

---
## 使用說明

### 1. 啟動程式
1. 開啟命令提示字元或 PowerShell，並切換到專案根目錄（包含 `autovideo.py` 的資料夾）。
2. 執行下列指令啟動程式：
   ```powershell
   python autovideo.py
   ```
3. 執行後會出現工具的圖形使用介面。

### 2. 操作流程
- **添加檔案：**  
  在介面中點擊「添加檔案」按鈕，選擇您要壓縮的影片檔案（可一次選擇多個檔案）。
- **設定輸出：**  
  - 點擊「瀏覽」按鈕選擇壓縮後影片的輸出資料夾。
  - 輸入目標檔案大小（單位：MB），此數值將用以控制壓縮品質與最終檔案大小。
- **開始轉換：**  
  點擊「開始轉換」按鈕後，程式將依序處理每個檔案，並在下方的狀態區顯示轉換進度與詳細狀態資訊。

### 3. 完成轉換
- 當所有檔案處理完成後，程式會顯示完成訊息。
- 請前往您設定的輸出資料夾查看轉換後的影片檔案。

---

## 打包成獨立執行檔（選用）
若您希望將此工具打包成不需要 Python 環境即可執行的獨立應用程式，可以使用 [PyInstaller](https://www.pyinstaller.org/)：
1. **安裝 PyInstaller：**
   ```powershell
   pip install pyinstaller
   ```
2. **打包工具：**
   在命令提示字元或 PowerShell 中切換到專案根目錄，然後執行下列指令：
   ```powershell
   pyinstaller --onefile --windowed --clean --exclude-module torch --exclude-module torchvision --hidden-import PIL autovideo.py
   ```
3. 打包完成後，生成的執行檔將會位於 `dist` 資料夾中。

---

## 常見問題

- **找不到 ffmpeg？**  
  本工具利用 pip 安裝的 imageio-ffmpeg 自動管理 ffmpeg，請確保已正確安裝 imageio-ffmpeg 套件。若有疑問，可嘗試更新：
  ```powershell
  pip install --upgrade imageio-ffmpeg
  ```

- **壓縮後影片檔案大小不符預期？**  
  壓縮後的影片大小受原始影片品質、解析度與編碼參數影響。建議您根據實際情況調整目標檔案大小參數。

- **程式執行出現錯誤？**  
  請確認命令提示字元中顯示的錯誤訊息，常見問題包括檔案路徑錯誤或套件未安裝完全。若無法解決，可嘗試重新安裝相關套件。

---

## 附加說明
- 無論您是否熟悉 Python，本說明都提供了從安裝 Python、下載程式碼、安裝套件到執行程式的每一步詳細指導。
- 若有任何疑問或需要幫助，歡迎與作者聯繫或參考相關 Python 基礎教程。

希望這個工具能幫助您輕鬆完成影片壓縮任務，謝謝使用！
