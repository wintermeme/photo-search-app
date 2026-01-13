import streamlit as st
import pandas as pd

# --- 页面配置 ---
st.set_page_config(page_title="图库搜索工具", layout="wide")

# --- 标题 ---
st.title("📂 在线图库搜索下载")

# --- 1. 加载数据 (带缓存，速度极快) ---
@st.cache_data
def load_data():
    try:
        # 读取 Excel
        df = pd.read_excel("data.xlsx")
        # 强制转为字符串
        df['name'] = df['name'].astype(str)
        df['url'] = df['url'].astype(str)
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return pd.DataFrame()

df = load_data()

# --- 2. 侧边栏：搜索控制 ---
with st.sidebar:
    st.header("🔍 搜索选项")
    # 搜索框
    search_term = st.text_input("输入关键词:", "")
    
    # 结果数量限制 (防止网页卡死)
    max_items = st.slider("显示数量限制", 10, 200, 50)
    
    st.write(f"数据库共有: {len(df)} 条图片")
    st.info("提示：输入关键词后按回车即可搜索。")

# --- 3. 筛选逻辑 ---
if search_term:
    # 模糊搜索
    results = df[df['name'].str.contains(search_term, case=False, na=False)]
else:
    # 如果没搜，就显示前几条
    results = df.head(max_items)

# --- 4. 展示画廊 ---
if not results.empty:
    st.success(f"找到 {len(results)} 个结果 (仅显示前 {min(len(results), max_items)} 个)")
    
    # 截取前 N 个，防止浏览器崩溃
    display_results = results.head(max_items)

    # 设置列数 (自适应布局)
    # 比如一行显示 4 张
    cols = st.columns(4) 
    
    for index, (idx, row) in enumerate(display_results.iterrows()):
        # 计算当前图片应该放在第几列
        col = cols[index % 4]
        
        with col:
            # 显示图片
            try:
                # use_column_width=True 让图片自动适应列宽
                st.image(row['url'], caption=row['name'], use_container_width=True)
                
                # 下载/查看链接
                # 网页版最简单的下载方式是提供直链，用户右键另存为
                st.link_button(f"⬇️ 下载/查看原图", row['url'])
                
            except Exception:
                st.error("图片加载失败")
            
            st.write("---") # 分割线
else:
    st.warning("没有找到相关图片")