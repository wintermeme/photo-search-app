import streamlit as st
import pandas as pd
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="Image Gallery Search", layout="wide")

# --- 2. Data Loading (Cached for Speed) ---
@st.cache_data
def get_data(file_mtime):  # <--- 第二处：在这里增加一个参数 file_mtime
    try:
        df = pd.read_excel("data.xlsx", engine="openpyxl", usecols=['name', 'url'])
        df['name'] = df['name'].astype(str)
        df['url'] = df['url'].astype(str)
        return df
    except Exception as e:
        st.error("Failed to load data.")
        return pd.DataFrame()

# 【改动3：在获取数据前，先读取文件的修改时间】
target_file = "data.xlsx"
mtime = os.path.getmtime(target_file) if os.path.exists(target_file) else 0
df = get_data(mtime) # 传入时间戳，文件变了时间戳就变，缓存就会自动刷新

# --- 3. Search Interface ---
st.title("⚡ Fast Image Search")
search_term = st.text_input("🔍 Type your keyword here:", "").strip()

# --- 4. Main Logic ---
if search_term:
    # Rapid filtering based on 'name'
    results = df[df['name'].str.contains(search_term, case=False, na=False)].copy()
    
    if not results.empty:
        # Limit display to 40 items to ensure page responsiveness
        display_limit = 40
        display_results = results.head(display_limit)
        
        # Action Bar: Summary
        st.success(f"Found {len(results)} results")
        
        # Provide a text area for batch link copying (The most efficient way for bulk download)
        with st.expander("📋 Copy all image links for Batch Download", expanded=False):
            all_links = "\n".join(results['url'].tolist())
            st.text_area("Copy and paste these links into your download manager (like IDM or FDM):", 
                         value=all_links, height=150)

        st.divider()

        # --- 5. Grid Preview (Optimized Rendering) ---
        cols_per_row = 4
        for i in range(0, len(display_results), cols_per_row):
            cols = st.columns(cols_per_row)
            batch = display_results.iloc[i : i + cols_per_row]
            
            for j, (idx, row) in enumerate(batch.iterrows()):
                with cols[j]:
                    # Using width="stretch" to match Streamlit 1.52+ requirements
                    st.image(row['url'], caption=row['name'], width="stretch")
                    
                    # Direct Link Button for fast individual download
                    st.link_button("💾 Download", row['url'], use_container_width=True)
                    st.write("---")
        
        if len(results) > display_limit:
            st.warning(f"Showing first {display_limit} results. Please refine your search for more specific images.")
            
    else:
        st.warning(f"No results found for '{search_term}'.")
else:

    st.info("Please enter a keyword to start searching for images.")

