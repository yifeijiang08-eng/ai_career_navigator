import streamlit as st

st.set_page_config(page_title="🔍 极简隔离测试", layout="wide")

st.title("🔍 Streamlit 运行状态生死测试")
st.write("如果这个页面点击有反应，说明问题出在 AI 服务或网络连接上；如果连这个都没反应，说明云端环境彻底坏了。")

# 测试状态与按钮点击
if "click_count" not in st.session_state:
    st.session_state["click_count"] = 0

if st.button("👉 点我测试点击反应 (不需要AI)", type="primary"):
    st.session_state["click_count"] += 1

st.success(f"按钮已被成功触发了 {st.session_state['click_count']} 次！")