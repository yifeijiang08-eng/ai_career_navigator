import streamlit as st
from ai_service import AIService

# ==================== 1. 页面全局配置 ====================
st.set_page_config(
    page_title="🧭 AI Career Navigator Pro",
    page_icon="🧭",
    layout="wide"
)

# 缓存并初始化 AI 服务
@st.cache_resource
def get_ai_service():
    return AIService()

ai = get_ai_service()

# 初始化全局状态
if "page" not in st.session_state:
    st.session_state["page"] = "industry_explore"
if "selected_industry" not in st.session_state:
    st.session_state["selected_industry"] = "AI"
if "selected_position" not in st.session_state:
    st.session_state["selected_position"] = "AI Agent工程师"
if "compare_list" not in st.session_state:
    st.session_state["compare_list"] = []

# ==================== 2. 侧边栏导航（极简解耦版） ====================
with st.sidebar:
    st.title("🧭 Career Navigator")
    st.markdown("### 🌟 求职全链路终端")
    
    # 使用按钮替代 radio，彻底杜绝状态冲突和死锁！
    if st.button("🎯 行业探索", use_container_width=True):
        st.session_state["page"] = "industry_explore"
        st.rerun()
        
    if st.button("🗺️ 职业地图 (Tree)", use_container_width=True):
        st.session_state["page"] = "explore_map"
        st.rerun()
        
    if st.button("📌 岗位详情", use_container_width=True):
        st.session_state["page"] = "position_detail"
        st.rerun()
        
    if st.button("🏢 公司情报", use_container_width=True):
        st.session_state["page"] = "company_detail"
        st.rerun()
        
    if st.button("📊 JD 技能分析", use_container_width=True):
        st.session_state["page"] = "jd_analysis"
        st.rerun()
        
    if st.button("⚖️ 岗位横向对比", use_container_width=True):
        st.session_state["page"] = "position_compare"
        st.rerun()

    st.markdown("---")
    if st.button("🔄 清空所有缓存与重置", use_container_width=True):
        st.cache_data.clear()
        st.session_state.clear()
        st.rerun()

# ==================== 3. 主界面可视化渲染 ====================
current_page = st.session_state["page"]

# ----------------- 模块 A：行业探索 -----------------
if current_page == "industry_explore":
    st.title("🎯 行业求职罗盘与生态探索")
    user_industry = st.text_input("输入你想探索的行业方向：", value="AI")

    if st.button("🚀 生成行业全景导航", type="primary", key="btn_gen_ind"):
        with st.spinner("正在生成行业全景..."):
            st.session_state["nav_data"] = ai.career_nav(user_industry)

    if "nav_data" in st.session_state and "error" not in st.session_state["nav_data"]:
        data = st.session_state["nav_data"]
        st.success(f"成功加载：{data.get('industry', user_industry)}")
        st.write(data.get("overview", ""))
        
        for idx, pos in enumerate(data.get("positions", [])):
            title = pos.get('title')
            st.markdown(f"### 📌 {title}")
            st.write(pos.get('description'))
            if st.button(f"🔍 深度剖析 {title}", key=f"p_jump_{idx}"):
                st.session_state["selected_position"] = title
                st.session_state["page"] = "position_detail"
                st.rerun()

# ----------------- 模块 B：职业地图 -----------------
elif current_page == "explore_map":
    st.title("🗺️ 动态职业生态树")
    industry = st.session_state.get("selected_industry", "AI")
    tree_data = ai.explore_tree(industry)
    
    if "error" in tree_data:
        st.error("生成职业树失败，请检查 API Key 配置。")
    else:
        st.json(tree_data)

# ----------------- 模块 C：岗位详情 -----------------
elif current_page == "position_detail":
    st.title("📌 目标岗位深度解析看板")
    pos_name = st.session_state.get("selected_position", "AI Agent工程师")
    st.markdown(f"当前锁定岗位：**{pos_name}**")
    
    pos_data = ai.position_detail(pos_name)
    if "error" in pos_data:
        st.error("获取岗位详情失败，请检查 API Key。")
    else:
        st.json(pos_data)

# ----------------- 模块 D：公司情报 -----------------
elif current_page == "company_detail":
    st.title("🏢 目标公司情报与内幕看板")
    comp_name = st.text_input("输入公司名称：", value="OpenAI")
    if st.button("查询情报"):
        st.json(ai.company_detail(comp_name))

# ----------------- 模块 E：JD 分析 -----------------
elif current_page == "jd_analysis":
    st.title("📊 JD 高频技能与简历优化")
    jd = st.text_area("粘贴 JD 原文：")
    if st.button("一键解析"):
        st.json(ai.jd_analysis(jd))

# ----------------- 模块 F：岗位对比 -----------------
elif current_page == "position_compare":
    st.title("⚖️ 岗位横向对比")
    st.write(st.session_state.get("compare_list", []))
