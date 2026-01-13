import streamlit as st
import pandas as pd

# --- 1. 极速页面配置 ---
st.set_page_config(page_title="图库极速版", layout="wide")

# --- 2. 缓存数据读取 (仅索引) ---
@st.cache_data
def get_data():
    try:
        # 指定列读取，减少内存占用，提升加载速度
        df = pd.read_excel("data.xlsx", engine="openpyxl", usecols=['name', 'url'])
        return df
    except Exception as e:
        st.error("数据加载失败，请检查 data.xlsx 是否在根目录")
        return pd.DataFrame()

df = get_data()

# --- 3. 搜索界面 ---
st.title("⚡ 图库极速搜索")
search_term = st.text_input("🔍 立即输入搜索：", "").strip()

# --- 4. 核心逻辑 ---
if search_term:
    # 快速筛选
    results = df[df['name'].str.contains(search_term, case=False, na=False)].copy()
    
    if not results.empty:
        # 只显示前 40 条以确保网页响应秒开
        display_results = results.head(40)
        
        # 顶部操作栏：一键全选下载提示
        st.success(f"找到 {len(results)} 条结果")
        st.info("💡 提示：预览后点击下方按钮可直接跳转下载。")

        # --- 5. 栅格预览 (优化渲染速度) ---
        cols_per_row = 4
        for i in range(0, len(display_results), cols_per_row):
            cols = st.columns(cols_per_row)
            batch = display_results.iloc[i : i + cols_per_row]
            
            for j, (idx, row) in enumerate(batch.iterrows()):
                with cols[j]:
                    # 关键：使用 width="stretch" 适配 1.52+ 版本
                    st.image(row['url'], caption=row['name'], width="stretch")
                    
                    # 极速下载：直接利用 link_button 触发
                    st.link_button("💾 下载图片", row['url'], use_container_width=True)
                    st.write("---")
    else:
        st.warning("无搜索结果")
else:
    st.info("请输入关键词，系统将实时筛选图片。")