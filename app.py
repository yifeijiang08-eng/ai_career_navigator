import streamlit as st
from ai_service import AIService

# 页面基本配置
st.set_page_config(
    page_title="AI 职场与求职全景导航",
    page_icon="🧭",
    layout="wide"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding-top: 1rem;
    }
    h1, h2, h3 {
        color: #1f2937;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

ai = AIService()

if "current_page" not in st.session_state:
    st.session_state.current_page = "行业全景导航"

# ================= 侧边栏菜单 =================
with st.sidebar:
    st.markdown("### 🧭 导航菜单")
    st.markdown("<p style='font-size: 13px; color: #6b7280;'>请选择功能模块：</p>", unsafe_allow_html=True)
    
    nav_items = [
        ("📈 行业全景导航", "行业全景导航"),
        ("🌳 职业生态树", "职业生态树"),
        ("🎯 岗位深度解析", "岗位深度解析"),
        ("🏢 公司情报站", "公司情报站"),
        ("📝 JD 简历优化", "JD 简历优化")
    ]
    
    for label, page_key in nav_items:
        is_selected = st.session_state.current_page == page_key
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
            
    st.markdown("---")
    st.info("💡 提示：请确保已在 Streamlit Cloud 后台的 Secrets 中正确配置了 `HUNYUAN_API_KEY`。")

# ================= 主界面 =================
page = st.session_state.current_page

if page == "行业全景导航":
    st.markdown("## 📈 行业求职全景导航")
    industry = st.text_input("请输入您关注的行业（例如：人工智能、大模型产品、新能源汽车）：", "人工智能")
    
    if st.button("生成行业全景报告", type="primary"):
        with st.spinner("AI 正在深度剖析行业全景及热招企业，请稍候..."):
            res = ai.career_nav(industry)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生成成功！")
                st.session_state["last_career_result"] = res

    # 如果已有生成结果，展示城市筛选与岗位/公司信息
    if "last_career_result" in st.session_state:
        res = st.session_state["last_career_result"]
        st.markdown(f"### 🌐 {res.get('industry', industry)} - 行业概览")
        st.info(res.get('overview', ''))
        
        # 收集所有出现过的城市，供用户筛选
        positions = res.get('positions', [])
        all_cities = set()
        for pos in positions:
            for comp in pos.get('companies', []):
                if comp.get('city'):
                    all_cities.add(comp.get('city'))
        
        selected_city = "全部城市"
        if all_cities:
            city_list = ["全部城市"] + sorted(list(all_cities))
            selected_city = st.selectbox("📍 按城市筛选招聘公司：", city_list)

        st.markdown("### 💼 核心岗位与推荐求职企业")
        for pos in positions:
            with st.expander(f"📌 {pos.get('title')} (薪资: {pos.get('salary_level', '暂无')})"):
                st.write(f"**岗位职责**: {pos.get('description')}")
                col1, col2, col3 = st.columns(3)
                col1.metric("推荐指数", f"{pos.get('recommendation', {}).get('score', '85')}分")
                col2.metric("求职难度", pos.get('difficulty', '中'))
                col3.metric("市场需求", pos.get('market_demand', '旺盛'))
                st.write(f"**核心业务场景**: {pos.get('business')}")
                
                st.markdown("---")
                st.markdown("#### 🏢 推荐招聘公司及直达链接")
                companies = pos.get('companies', [])
                
                # 根据用户选择的城市进行过滤
                filtered_companies = [
                    c for c in companies 
                    if selected_city == "全部城市" or c.get('city') == selected_city
                ]
                
                if not filtered_companies:
                    st.caption("该岗位在当前选中城市暂无匹配的直推企业。")
                else:
                    for comp in filtered_companies:
                        c_col1, c_col2, c_col3 = st.columns([2, 1, 1])
                        with c_col1:
                            st.markdown(f"**{comp.get('name')}** <span style='color: gray; font-size: 12px;'>({comp.get('city', '全球/远程')})</span>", unsafe_allow_html=True)
                        with c_col2:
                            if comp.get('official_url'):
                                st.link_button("🌐 公司官网", comp.get('official_url'), use_container_width=True)
                        with c_col3:
                            if comp.get('linkedin_url'):
                                st.link_button("🔗 LinkedIn", comp.get('linkedin_url'), use_container_width=True)

elif page == "职业生态树":
    st.markdown("## 🌳 矩阵化职业生态树")
    industry = st.text_input("请输入要解构的行业：", "互联网大厂/大模型")
    if st.button("生成职业生态树", type="primary"):
        with st.spinner("AI 正在构建多维生态树..."):
            res = ai.explore_tree(industry)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生态树生成完毕！")
                if isinstance(res, dict):
                    for category, job_list in res.items():
                        st.markdown(f"#### 📂 {category}")
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

elif page == "岗位深度解析":
    st.markdown("## 🎯 岗位深度解析")
    pos_name = st.text_input("请输入具体岗位名称：", "大模型产品经理")
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
    company_name = st.text_input("请输入目标公司名称：", "字节跳动")
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
    jd_text = st.text_area("请粘贴目标岗位的 JD（招聘要求）原文：", height=200)
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