import streamlit as st
from ai_service import AIService
import pandas as pd

# ==================== 1. 页面全局配置与美化 ====================
st.set_page_config(
    page_title="🧭 AI Career Navigator Pro",
    page_icon="🧭",
    layout="wide"
)

# 注入自定义 CSS：实现现代卡片风、毛玻璃效果、炫酷边框与阴影
st.markdown("""
<style>
    /* 全局背景与字体微调 */
    .main {
        background-color: #f8fafc;
    }
    
    /* 现代高定卡片样式 */
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    
    /* 标题美化 */
    h1, h2, h3 {
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 侧边栏优化 */
    .css-1d391kg {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_ai_service():
    return AIService()

ai = get_ai_service()

# 初始化页面状态流转
if "page" not in st.session_state:
    st.session_state["page"] = "industry_explore"
if "selected_industry" not in st.session_state:
    st.session_state["selected_industry"] = "AI"
if "selected_position" not in st.session_state:
    st.session_state["selected_position"] = "AI Agent工程师"
if "selected_company" not in st.session_state:
    st.session_state["selected_company"] = "OpenAI"
if "compare_list" not in st.session_state:
    st.session_state["compare_list"] = []

# ==================== 2. 侧边栏导航 ====================
with st.sidebar:
    st.title("🧭 Career Navigator")
    st.markdown("### 🌟 求职全链路终端")
    
    menu = st.radio("导航菜单", [
        "🎯 行业探索", 
        "🗺️ 职业地图 (Tree)", 
        "📌 岗位详情", 
        "🏢 公司情报", 
        "📊 JD 技能分析",
        "⚖️ 岗位横向对比"
    ])
    
    # 路由映射
    menu_mapping = {
        "🎯 行业探索": "industry_explore",
        "🗺️ 职业地图 (Tree)": "explore_map",
        "📌 岗位详情": "position_detail",
        "🏢 公司情报": "company_detail",
        "📊 JD 技能分析": "jd_analysis",
        "⚖️ 岗位横向对比": "position_compare"
    }
    st.session_state["page"] = menu_mapping[menu]

    st.markdown("---")
    if st.button("🔄 清空所有缓存与重置", use_container_width=True):
        st.cache_data.clear()
        st.session_state.clear()
        st.rerun()

# ==================== 3. 主界面可视化渲染 ====================

# ----------------- 模块 A：行业探索 -----------------
if st.session_state["page"] == "industry_explore":
    st.title("🎯 行业求职罗盘与生态探索")
    st.markdown("输入或点击下方热门方向，5分钟极速掌握行业核心岗位、技术栈与代表企业。")
    st.markdown("---")

    preset_directions = ["AI", "机器人", "新能源", "游戏开发", "自动驾驶", "金融科技", "芯片", "跨境电商"]
    cols = st.columns(4)
    selected_preset = None
    for idx, d in enumerate(preset_directions):
        with cols[idx % 4]:
            if st.button(f"🔥 {d}", use_container_width=True):
                selected_preset = d

    user_industry = st.text_input("或者自定义输入你想探索的行业方向：", value=selected_preset if selected_preset else "AI")

    if st.button("🚀 生成行业全景导航", type="primary", use_container_width=True):
        st.session_state["selected_industry"] = user_industry
        with st.spinner(f"正在深度萃取【{user_industry}】行业全景（已启用极速缓存）..."):
            st.session_state["nav_data"] = ai.career_nav(user_industry)

    if "nav_data" in st.session_state and "error" not in st.session_state["nav_data"]:
        data = st.session_state["nav_data"]
        
        # 概览看板
        st.markdown(f"## 🌐 {data.get('industry')} 行业核心全景")
        st.info(f"**行业概览**: {data.get('overview')}")
        
        st.markdown("### 📌 核心岗位矩阵")
        positions = data.get("positions", [])
        
        for pos in positions:
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📌 {pos.get('title')} <span style="font-size:0.8rem; color:#64748b; float:right;">推荐度: {pos.get('recommendation', {}).get('score')} | 难度: {pos.get('difficulty')}</span></h3>
                    <p><em>{pos.get('description')}</em></p>
                    <p><b>市场需求</b>: {pos.get('market_demand')} &nbsp;|&nbsp; <b>薪资水平</b>: {pos.get('salary_level')}</p>
                    <p><b>主要业务</b>: {pos.get('business')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button(f"🔍 深度剖析此岗位", key=f"pos_{pos.get('title')}", use_container_width=True):
                        st.session_state["selected_position"] = pos.get('title')
                        st.session_state["page"] = "position_detail"
                        st.rerun()
                with col_btn2:
                    if st.button(f"➕ 加入横向对比", key=f"comp_{pos.get('title')}", use_container_width=True):
                        if pos.get('title') not in st.session_state["compare_list"]:
                            st.session_state["compare_list"].append(pos.get('title'))
                            st.success(f"已成功将 {pos.get('title')} 加入对比！")

        st.markdown("### ⚡ 推荐搜索关键词（一键复制）")
        kw = data.get("keywords", {})
        col_kw1, col_kw2 = st.columns(2)
        with col_kw1:
            st.markdown("**中文关键词**")
            st.code(", ".join(kw.get('cn', [])), language=None)
        with col_kw2:
            st.markdown("**英文关键词**")
            st.code(", ".join(kw.get('en', [])), language=None)

# ----------------- 模块 B：职业地图 (Explore Tree) -----------------
elif st.session_state["page"] == "explore_map":
    st.title("🗺️ 动态职业生态树 (Explore Tree)")
    industry = st.session_state.get("selected_industry", "AI")
    st.markdown(f"当前探索大方向：**{industry}** —— 由 AI 动态解构的矩阵化职业树：")
    st.markdown("---")

    tree_data = ai.explore_tree(industry)
    if "error" in tree_data:
        st.error("生成职业树失败，请重试。")
    else:
        cols = st.columns(len(tree_data))
        for idx, (category, sub_positions) in enumerate(tree_data.items()):
            with cols[idx]:
                st.markdown(f"""
                <div style="background:#f1f5f9; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:10px;">
                    ⚙️ {category}
                </div>
                """, unsafe_allow_html=True)
                for pos in sub_positions:
                    if st.button(f"👉 {pos}", use_container_width=True, key=f"tree_{pos}"):
                        st.session_state["selected_position"] = pos
                        st.session_state["page"] = "position_detail"
                        st.rerun()

# ----------------- 模块 C：岗位详情页 (Position) -----------------
elif st.session_state["page"] == "position_detail":
    st.title("📌 目标岗位深度解析看板")
    pos_name = st.session_state.get("selected_position", "AI Agent工程师")
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown(f"当前锁定：**{pos_name}**")
    with col_t2:
        if st.button("➕ 加入对比", use_container_width=True):
            if pos_name not in st.session_state["compare_list"]:
                st.session_state["compare_list"].append(pos_name)
                st.success("已加入对比！")

    st.markdown("---")
    pos_data = ai.position_detail(pos_name)
    
    if "error" in pos_data:
        st.error("获取岗位详情失败。")
    else:
        st.markdown(f"## 💡 {pos_data.get('title')}")
        st.markdown(f"> *{pos_data.get('overview')}*")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"💰 **薪资范围**: {pos_data.get('salary_range')}")
        with col_info2:
            st.markdown(f"📈 **成长路径**: {pos_data.get('growth_path')}")
        
        st.markdown("### 📋 核心岗位职责")
        for r in pos_data.get("responsibilities", []):
            st.markdown(f"- {r}")

        st.markdown("### 🔄 典型日常工作流程")
        for w in pos_data.get("workflow", []):
            st.markdown(f"1. {w}")

        st.markdown("### 🛠️ 必须掌握的核心技术栈（一键复制）")
        st.code("\n".join(pos_data.get("tech_stack", [])), language="python")

        st.markdown("### 💻 推荐练手项目")
        for p in pos_data.get("recommended_projects", []):
            st.markdown(f"- {p}")

        st.markdown("### 🎯 高频面试考察点")
        for i in pos_data.get("interview_tips", []):
            st.markdown(f"- {i}")

# ----------------- 模块 D：公司情报页 (Company) -----------------
elif st.session_state["page"] == "company_detail":
    st.title("🏢 目标公司情报与内幕看板")
    comp_name = st.text_input("输入你想查询的目标公司名称：", value=st.session_state.get("selected_company", "OpenAI"))
    
    if st.button("🔍 查询公司情报", type="primary"):
        st.session_state["selected_company"] = comp_name

    comp_data = ai.company_detail(st.session_state["selected_company"])
    
    if "error" in comp_data:
        st.error("获取公司情报失败。")
    else:
        st.markdown(f"# 🏢 {comp_data.get('name')}")
        st.markdown(f"> **公司介绍**: {comp_data.get('intro')}")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"💰 **薪资福利**: {comp_data.get('salary_benefits')}")
        with col_c2:
            st.markdown(f"📍 **办公城市**: {', '.join(comp_data.get('cities', []))}")
        
        st.markdown("### 🔗 官方招聘入口")
        for ch in comp_data.get("hiring_channels", []):
            st.markdown(f"- {ch}")

        st.markdown("### 🔥 当前热招岗位")
        for op in comp_data.get("open_positions", []):
            st.markdown(f"- {op}")

        st.markdown("### 💬 真实员工评价与面经风格")
        st.markdown(f"- **面试风格**: {comp_data.get('interview_experience')}")
        st.markdown(f"- **职场评价**: {comp_data.get('employee_review')}")

# ----------------- 模块 E：JD 高频技能分析 (JD) -----------------
elif st.session_state["page"] == "jd_analysis":
    st.title("📊 JD 高频技能与简历优化")
    st.markdown("粘贴心仪公司的招聘 JD 原文，AI 将为你瞬间剥离高频词、给出简历润色指南。")
    st.markdown("---")

    jd_input = st.text_area("在此粘贴岗位 JD 原文：", placeholder="例如：负责多模态大模型对齐与指令微调，熟悉 PyTorch...", height=150)
    
    if st.button("🚀 一键深度解析 JD", type="primary", use_container_width=True):
        if not jd_input.strip():
            st.warning("请输入 JD 内容！")
        else:
            with st.spinner("正在提炼高频技能与面试考点..."):
                st.session_state["jd_result"] = ai.jd_analysis(jd_input)

    if "jd_result" in st.session_state and "error" not in st.session_state["jd_result"]:
        jd_res = st.session_state["jd_result"]
        st.markdown(f"## 📋 岗位分析结果：{jd_res.get('job_title')}")
        
        st.markdown("### 🎯 核心考察能力")
        for comp in jd_res.get("core_competencies", []):
            st.markdown(f"- {comp}")

        st.markdown("### ⚡ 简历高频技能关键词（直接复制进简历）")
        skills_str = ", ".join(jd_res.get("high_frequency_skills", []))
        st.code(skills_str, language=None)

        st.markdown("### 💡 简历亮点包装建议")
        for tip in jd_res.get("resume_writing_tips", []):
            st.markdown(f"- {tip}")

        st.markdown("### 🔥 高频面试题预判")
        for q in jd_res.get("interview_questions", []):
            st.markdown(f"- {q}")

# ----------------- 模块 F：岗位横向对比 (Compare) -----------------
elif st.session_state["page"] == "position_compare":
    st.title("⚖️ 目标岗位横向多维对比")
    st.markdown("直观对比已加入收藏的多个目标岗位，辅助进行最优求职决策。")
    st.markdown("---")

    compare_list = st.session_state.get("compare_list", [])
    
    if not compare_list:
        st.warning("⚠️ 当前对比栏为空！请先在【行业探索】或【岗位详情】页面点击“加入对比”。")
    else:
        cols = st.columns(len(compare_list))
        for idx, pos_title in enumerate(compare_list):
            with cols[idx]:
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid #cbd5e1; padding:15px; border-radius:10px;">
                    <h3>📌 {pos_title}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                detail = ai.position_detail(pos_title)
                if "error" not in detail:
                    st.markdown(f"**薪资预期**: {detail.get('salary_range')}")
                    st.markdown(f"**成长空间**: {detail.get('growth_path')}")
                    st.markdown("**核心技术栈**:")
                    st.code("\n".join(detail.get("tech_stack", [])[:4]), language=None)
                
                if st.button(f"🗑️ 移除此岗位", key=f"rm_{pos_title}", use_container_width=True):
                    st.session_state["compare_list"].remove(pos_title)
                    st.rerun()