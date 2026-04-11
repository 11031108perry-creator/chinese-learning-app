import streamlit as st
import os
import pandas as pd

# 設定網頁基本樣式 (這行可以讓網頁預設變得更寬、更好看)
st.set_page_config(page_title="當代中文教學平台", layout="wide")

# 1. 設定網頁標題
st.title("📚 當代中文 數位閱讀平台")

# 2. 定義你的主資料夾名稱
base_folder = "當代中文"

# 3. 側邊欄目錄
st.sidebar.header("目錄選單")

# 檢查「當代中文」資料夾是否存在
if os.path.exists(base_folder):
    
    # 抓取裡面所有的冊數資料夾 (第一冊、第二冊...)
    volumes = sorted(os.listdir(base_folder))
    selected_volume = st.sidebar.selectbox("請選擇冊數：", volumes)
    
    if selected_volume:
        # 組合出被選中冊數的完整路徑
        volume_path = os.path.join(base_folder, selected_volume)
        
        # 抓取該冊裡面的所有 txt 檔案
        files = sorted([f for f in os.listdir(volume_path) if f.endswith('.txt')])
        selected_file = st.sidebar.selectbox("請選擇內容：", files)
        
        if selected_file:
            # 組合出文字檔的完整路徑
            file_path = os.path.join(volume_path, selected_file)
            
            # 在畫面上顯示目前選擇的檔案
            st.subheader(f"📖 目前顯示：{selected_file}")
            
            # 打開檔案並讀取內容
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # --- 判斷邏輯：如果是生詞檔，就轉成表格 ---
            if "生詞" in selected_file:
                data = []
                for line in lines:
                    # 去除前後空白
                    line = line.strip()
                    
                    # 略過空行，或是純粹寫著「生詞」的標題行
                    if not line or line == "生詞":
                        continue
                        
                    # 檢查這行是不是有包含 '.' (例如 "1. 安德思")
                    if "." in line:
                        # 用 '.' 來切割，並且只切第一次，分成「編號」跟「生詞」
                        parts = line.split(".", 1) 
                        if len(parts) == 2:
                            number = parts[0].strip()  # 取得編號
                            word = parts[1].strip()    # 取得生詞
                            data.append([number, word])
                
                # 將資料轉換成表格格式
                if data:
                    # 建立表格，明確指定這兩個欄位的名稱
                    df = pd.DataFrame(data, columns=["編號", "生詞"])
                    
                    # 使用 st.dataframe 並隱藏預設的索引 (讓畫面更乾淨)
                    st.dataframe(df, hide_index=True, use_container_width=True) 
                else:
                    st.warning("這個生詞檔好像沒有符合格式的生詞喔！")
            
            # --- 如果是課文檔，就直接顯示文字 ---
            else:
                # 將所有行合併成一大段文字
                content = "".join(lines)
                st.text_area(label="課文內容", value=content, height=400)

else:
    st.error(f"找不到「{base_folder}」資料夾，請確認它跟 app.py 放在同一個位置喔！")