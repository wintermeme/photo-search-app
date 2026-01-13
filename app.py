import streamlit as st
import pandas as pd

st.set_page_config(page_title="图库搜索工具", layout="wide")

# --- 1. 核心：快速读取索引 (仅加载表格，不加载图片) ---
@st.cache_data
def get_data_index():
    try:
        # 只读取必要的两列，进一步加快速度
        df = pd.read_excel("data.xlsx", engine="openpyxl", usecols=['name', 'url'])
        df['name'] = df['name'].astype(str)
        return df
    except Exception as e:
        st.error(f"索引加载失败: {e}")
        return pd.DataFrame()

df = get_data_index()

# --- 2. 界面设计 ---
st.title("📂 在线图库搜索")

# 搜索框放在页面顶部中央，更显眼
search_term = st.text_input("🔍 输入关键词搜索图片 (例如: '风景', '图标')", "").strip()

# --- 3. 搜索与渲染逻辑 ---
if search_term:
    # 仅在有输入时进行筛选
    results = df[df['name'].str.contains(search_term, case=False, na=False)]
    
    if not results.empty:
        st.write(f"找到 {len(results)} 个匹配结果：")
        
        # 限制单次显示数量，避免网络请求过多导致崩溃
        display_count = 40 
        display_results = results.head(display_count)

        # 栅格布局
        cols = st.columns(4) 
        for index, (idx, row) in enumerate(display_results.iterrows()):
            with cols[index % 4]:
                # 关键：只有走到这一行，Streamlit 才会去请求这个 URL 的图片
                st.image(row['url'], caption=row['name'], width='stretch')
                st.link_button("查看原图", row['url'])
                st.write("---")
        
        if len(results) > display_count:
            st.info(f"结果较多，已自动为您截取前 {display_count} 张。请尝试缩短关键词。")
    else:
        st.warning("未找到匹配的图片，请换个词试试。")
else:
    # 默认状态：不加载图片，只显示欢迎语或操作提示
    st.info("👆 请在上方输入关键词开始搜索。")
    # 展示几个示例（可选）
    st.write("您可以尝试搜索：", ", ".join(df['name'].head(5).tolist()))