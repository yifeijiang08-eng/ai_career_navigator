import streamlit as st
from ai_service import AIService

# 页面基本配置
st.set_page_config(
    page_title="AI 职场与求职全景导航",
    page_icon="🧭",
    layout="wide"
)

# 自定义 CSS 样式，打造长方形卡片按键和现代感 UI
st.markdown("""
<style>
    /* 侧边栏整体背景与美化 */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding-top: 1rem;
    }
    
    /* 统一调整主界面标题样式 */
    h1, h2, h3 {
        color: #1f2937;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 卡片式容器美化 */
    .st-emotion-cache-1r7slds {
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 AI 服务
ai = AIService()

# 使用 Streamlit 的 session_state 来记录当前选中的功能模块
if "current_page" not in st.session_state:
    st.session_state.current_page = "行业全景导航"

# ================= 侧边栏设计（长方形卡片按钮） =================
with st.sidebar:
    st.markdown("### 🧭 导航菜单")
    st.markdown("<p style='font-size: 13px; color: #6b7280;'>请选择功能模块：</p>", unsafe_allow_html=True)
    
    # 定义功能列表
    nav_items = [
        ("📈 行业全景导航", "行业全景导航"),
        ("🌳 职业生态树", "职业生态树"),
        ("🎯 岗位深度解析", "岗位深度解析"),
        ("🏢 公司情报站", "公司情报站"),
        ("📝 JD 简历优化", "JD 简历优化")
    ]
    
    # 渲染长方形卡片式按键
    for label, page_key in nav_items:
        # 用不同的按钮样式来模拟卡片点击
        is_selected = st.session_state.current_page == page_key
        button_type = "primary" if is_selected else "secondary"
        
        # 利用全宽按钮呈现长方形卡片效果
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
            
    st.markdown("---")
    st.info("💡 提示：请确保已在 Streamlit Cloud 后台的 Secrets 中正确配置了 `HUNYUAN_API_KEY`。")

# ================= 主界面内容渲染 =================
page = st.session_state.current_page

if page == "行业全景导航":
    st.markdown("## 📈 行业求职全景导航")
    industry = st.text_input("请输入您关注的行业（例如：人工智能、大模型产品、新能源汽车）：", "人工智能")
    
    if st.button("生成行业全景报告", type="primary"):
        with st.spinner("AI 正在深度剖析行业全景，请稍候..."):
            res = ai.career_nav(industry)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生成成功！")
                st.markdown(f"### 🌐 {res.get('industry', industry)} - 行业概览")
                st.info(res.get('overview', ''))
                
                st.markdown("### 💼 核心岗位矩阵")
                positions = res.get('positions', [])
                for pos in positions:
                    with st.expander(f"📌 {pos.get('title')} (薪资: {pos.get('salary_level', '暂无')})"):
                        st.write(f"**岗位职责**: {pos.get('description')}")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("推荐指数", f"{pos.get('recommendation', {}).get('score', '85')}分")
                        col2.metric("求职难度", pos.get('difficulty', '中'))
                        col3.metric("市场需求", pos.get('market_demand', '旺盛'))
                        st.write(f"**核心业务场景**: {pos.get('business')}")

elif page == "职业生态树":
    st.markdown("## 🌳 矩阵化职业生态树")
    st.markdown("探索目标行业的细分方向与岗位演进路线图。")
    industry = st.text_input("请输入要解构的行业：", "互联网大厂/大模型")
    
    if st.button("生成职业生态树", type="primary"):
        with st.spinner("AI 正在构建多维生态树..."):
            res = ai.explore_tree(industry)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生态树生成完毕！")
                st.markdown("### 🌲 行业职业图谱")
                
                # 美化生态树展示：将原本的 JSON 变成卡片网格与层级结构
                if isinstance(res, dict):
                    for category, job_list in res.items():
                        with st.container():
                            st.markdown(f"#### 📂 {category}")
                            # 用列排布岗位，视觉上更像树状分支
                            if isinstance(job_list, list) and job_list:
                                cols = st.columns(min(len(job_list), 3))
                                for idx, job in enumerate(job_list):
                                    with cols[idx % len(cols)]:
                                        st.markdown(
                                            f"""
                                            <div style="padding: 10px 15px; margin-bottom: 8px; background-color: #f0f2f6; border-left: 4px solid #3b82f6; border-radius: 4px; font-size: 14px; font-weight: 500;">
                                                🌿 {job}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                            st.markdown("---")
                else:
                    st.write(res)

elif page == "岗位深度解析":
    st.markdown("## 🎯 岗位深度解析")
    pos_name = st.text_input("请输入具体岗位名称（例如：大模型算法工程师、产品经理）：", "大模型产品经理")
    if st.button("开始深度剖析", type="primary"):
        with st.spinner("AI 正在拆解岗位技能栈与面试考点..."):
            res = ai.position_detail(pos_name)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("解析成功！")
                st.markdown(f"### 📋 {res.get('title', pos_name)}")
                st.info(res.get('overview', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🛠️ 核心技术栈 / 能力要求")
                    for tech in res.get('tech_stack', []):
                        st.markdown(f"- {tech}")
                        
                    st.markdown("#### 📝 日常工作流")
                    for wf in res.get('workflow', []):
                        st.markdown(f"- {wf}")
                        
                with col2:
                    st.markdown("#### 🚀 推荐练手项目")
                    for proj in res.get('recommended_projects', []):
                        st.markdown(f"- {proj}")
                        
                    st.markdown("#### 💡 高频面试考点")
                    for tip in res.get('interview_tips', []):
                        st.markdown(f"- {tip}")

elif page == "公司情报站":
    st.markdown("## 🏢 公司情报站")
    company_name = st.text_input("请输入目标公司名称（例如：腾讯、OpenAI、字节跳动）：", "字节跳动")
    if st.button("获取公司情报", type="primary"):
        with st.spinner("正在搜集公司情报与内幕..."):
            res = ai.company_detail(company_name)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("情报获取成功！")
                st.markdown(f"### 🏢 {res.get('name', company_name)}")
                st.write(res.get('intro', ''))
                st.markdown(f"**💰 薪资福利特点**: {res.get('salary_benefits', '')}")
                st.markdown(f"**🎯 面试风格**: {res.get('interview_experience', '')}")

elif page == "JD 简历优化":
    st.markdown("## 📝 JD 简历与面试优化")
    jd_text = st.text_area("请粘贴目标岗位的 JD（招聘要求）原文：", height=200, placeholder="在此粘贴招聘 JD...")
    if st.button("开始诊断与优化建议", type="primary"):
        if not jd_text.strip():
            st.warning("请先输入有效的 JD 内容！")
        else:
            with st.spinner("AI 正在逐字分析 JD 关键词..."):
                res = ai.jd_analysis(jd_text)
                if "error" in res:
                    st.error(f"调用出错: {res['error']}")
                else:
                    st.success("分析完成！")
                    st.markdown("### 🔍 核心竞争力与高频词")
                    for skill in res.get('high_frequency_skills', []):
                        st.markdown(f"`{skill}`", unsafe_allow_html=True)
                    
                    st.markdown("### 📈 简历包装建议")
                    for tip in res.get('resume_writing_tips', []):
                        st.markdown(f"- {tip}")