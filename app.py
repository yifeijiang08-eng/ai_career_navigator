import streamlit as st
from ai_service import AIService

# 1. 页面基本配置
st.set_page_config(
    page_title="🧭 AI Career Navigator - 智能求职与职业规划导师",
    page_icon="🧭",
    layout="wide"
)

# 2. 初始化 AI 服务（使用缓存防止重复初始化）
@st.cache_resource
def get_ai_service():
    return AIService()

ai = get_ai_service()

# 3. 页面侧边栏：功能导航与输入
st.sidebar.title("🧭 导航菜单")
tab_choice = st.sidebar.radio(
    "请选择功能模块：",
    ["行业全景导航", "职业生态树", "岗位深度解析", "公司情报站", "JD 简历优化"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：请确保已在 Streamlit Cloud 后台的 Secrets 中正确配置了 `GEMINI_API_KEY`。")

# 4. 主界面逻辑
st.title("🧭 AI 职场与求职全景导航专家")
st.markdown("基于 **Google Gemini 1.5 Flash** 驱动，为您提供全方位的求职与职业发展决策支持。")
st.markdown("---")

# --- 模块一：行业全景导航 ---
if tab_choice == "行业全景导航":
    st.header("📈 行业求职全景导航")
    industry_input = st.text_input("请输入您关注的行业（例如：人工智能、大模型产品、新能源汽车）：", "人工智能")
    
    if st.button("生成行业全景报告", type="primary"):
        if not industry_input:
            st.warning("请输入行业名称！")
        else:
            with st.spinner("AI 正在深度分析行业趋势与核心岗位，请稍候..."):
                result = ai.career_nav(industry_input)
                if "error" in result:
                    st.error(f"调用出错: {result['error']}")
                else:
                    st.subheader(f"📊 【{result.get('industry', industry_input)}】行业概览")
                    st.write(result.get("overview", ""))
                    
                    st.subheader("🔥 核心岗位矩阵")
                    positions = result.get("positions", [])
                    for pos in positions:
                        with st.expander(f"📌 {pos.get('title')} (难度: {pos.get('difficulty')} | 市场需求: {pos.get('market_demand')})"):
                            st.write(f"**岗位职责**: {pos.get('description')}")
                            st.write(f"**薪资范围**: {pos.get('salary_level')}")
                            st.write(f"**核心业务场景**: {pos.get('business')}")
                    
                    st.subheader("🔑 搜索关键词推荐")
                    keywords = result.get("keywords", {})
                    st.write("**中文关键词**: ", ", ".join(keywords.get("cn", [])))
                    st.write("**英文关键词**: ", ", ".join(keywords.get("en", [])))

# --- 模块二：职业生态树 ---
elif tab_choice == "职业生态树":
    st.header("🌳 矩阵化职业生态树")
    industry_input = st.text_input("请输入行业方向（例如：互联网金融、半导体）：", "互联网大厂")
    
    if st.button("生成职业生态树", type="primary"):
        with st.spinner("AI 正在构建生态树..."):
            result = ai.explore_tree(industry_input)
            if "error" in result:
                st.error(f"调用出错: {result['error']}")
            else:
                st.json(result)

# --- 模块三：岗位深度解析 ---
elif tab_choice == "岗位深度解析":
    st.header("🔍 岗位深度解析与面试指南")
    pos_input = st.text_input("请输入具体岗位名称（例如：大模型算法工程师、高级产品经理）：", "大模型算法工程师")
    
    if st.button("开始深度解析", type="primary"):
        with st.spinner("AI 正在拆解岗位技能与面试考点..."):
            result = ai.position_detail(pos_input)
            if "error" in result:
                st.error(f"调用出错: {result['error']}")
            else:
                st.subheader(f"🎯 岗位：{result.get('title')}")
                st.write(f"**一句话总结**: {result.get('overview')}")
                st.write(f"**薪资范围**: {result.get('salary_range')}")
                st.write(f"**晋升路径**: {result.get('growth_path')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📋 核心职责")
                    for r in result.get("responsibilities", []):
                        st.markdown(f"- {r}")
                    st.markdown("### 🛠️ 所需技术栈")
                    for t in result.get("tech_stack", []):
                        st.markdown(f"- {t}")
                with col2:
                    st.markdown("### 🚀 推荐练手项目")
                    for p in result.get("recommended_projects", []):
                        st.markdown(f"- {p}")
                    st.markdown("### 💡 高频面试考点")
                    for tip in result.get("interview_tips", []):
                        st.markdown(f"- {tip}")

# --- 模块四：公司情报站 ---
elif tab_choice == "公司情报站":
    st.header("🏢 目标公司求职情报")
    company_input = st.text_input("请输入公司名称（例如：字节跳动、OpenAI、腾讯）：", "字节跳动")
    
    if st.button("获取公司情报", type="primary"):
        with st.spinner("AI 正在搜集公司内幕与面试风格..."):
            result = ai.company_detail(company_input)
            if "error" in result:
                st.error(f"调用出错: {result['error']}")
            else:
                st.subheader(f"🏢 {result.get('name')}")
                st.write(result.get("intro"))
                st.write(f"**薪资福利**: {result.get('salary_benefits')}")
                st.write(f"**主要城市**: {', '.join(result.get('cities', []))}")
                st.write(f"**面试风格**: {result.get('interview_experience')}")
                st.write(f"**职场评价**: {result.get('employee_review')}")

# --- 模块五：JD 简历优化 ---
elif tab_choice == "JD 简历优化":
    st.header("📝 招聘 JD 智能分析与简历优化")
    jd_input = st.text_area("请粘贴你要应聘的岗位 JD 原文：", height=200, placeholder="在此粘贴招聘要求...")
    
    if st.button("智能分析 JD", type="primary"):
        if not jd_input.strip():
            st.warning("请先粘贴 JD 原文！")
        else:
            with st.spinner("AI 正在进行词频提取与简历包装指导..."):
                result = ai.jd_analysis(jd_input)
                if "error" in result:
                    st.error(f"调用出错: {result['error']}")
                else:
                    st.subheader(f"🎯 识别岗位: {result.get('job_title')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🧠 核心能力要求")
                        for c in result.get("core_competencies", []):
                            st.markdown(f"- {c}")
                        st.markdown("### 🔥 高频技能词")
                        for s in result.get("high_frequency_skills", []):
                            st.markdown(f"- `{s}`")
                    with col2:
                        st.markdown("### ✨ 简历包装建议")
                        for tip in result.get("resume_writing_tips", []):
                            st.markdown(f"- {tip}")
                        st.markdown("### ❓ 可能面临的面试题")
                        for q in result.get("interview_questions", []):
                            st.markdown(f"- {q}")