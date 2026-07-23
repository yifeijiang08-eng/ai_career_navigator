import streamlit as st
from ai_service import AIService

# 页面基本配置
st.set_page_config(
    page_title="AI 职场与求职全景导航",
    page_icon="🧭",
    layout="wide"
)

# ================= 极简高级浅绿色与白色 SaaS 风格 CSS 注入 =================
st.markdown("""
<style>
    .stApp {
        background-color: #f4f8f6;
        color: #2c3e50;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #eaf2ed;
        border-right: 1px solid #d5e5dc;
    }
    h1, h2, h3, h4 {
        color: #1b4332 !important;
        font-weight: 700;
    }
    .raised-card {
        background: #ffffff;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(44, 122, 92, 0.08);
        border: 1px solid #d8e8df;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .raised-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(44, 122, 92, 0.12);
    }
    .hiring-badge {
        display: inline-flex;
        align-items: center;
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #c8e6c9;
    }
    .green-dot {
        height: 8px;
        width: 8px;
        background-color: #4caf50;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        box-shadow: 0 0 6px #4caf50;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #ffffff !important;
        border: 1px solid #cce3d4 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

ai = AIService()

# 初始化 Session State 以实现模块强联动
if "current_page" not in st.session_state:
    st.session_state.current_page = "行业全景导航"
if "target_position" not in st.session_state:
    st.session_state.target_position = "大模型产品经理"
if "target_company" not in st.session_state:
    st.session_state.target_company = "OpenAI"

# ================= 侧边栏导航菜单 =================
with st.sidebar:
    st.markdown("### 🧭 导航菜单")
    st.markdown("<p style='font-size: 13px; color: #52796f;'>多维联动求职系统</p>", unsafe_allow_html=True)
    
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
    st.info("💡 提示：所有模块已实现完美联动。点击任意岗位或公司，系统将精准同步对应数据！")

# ================= 主页面逻辑渲染 =================
page = st.session_state.current_page

# ---------------- 1. 行业全景导航 ----------------
if page == "行业全景导航":
    st.markdown("## 📈 行业求职全景导航")
    st.markdown("<p style='color: #52796f;'>支持结合跨界背景（如小语种、金融、法律等）深度挖掘 AI 行业切入点。</p>", unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns([2, 1])
    with col_i1:
        industry = st.text_input("请输入目标行业：", "人工智能 / 大模型")
    with col_i2:
        cross_skill = st.text_input("跨界背景/附加技能（可选）：", "小语种 / 语言学背景")
        
    if st.button("生成行业全景与企业猎头库", type="primary"):
        with st.spinner("AI 正在深度绘制行业全景图谱，甄选大厂及小而美高成长企业..."):
            res = ai.career_nav(industry, cross_skill)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生成完毕！")
                st.session_state["last_career_result"] = res

    if "last_career_result" in st.session_state:
        res = st.session_state["last_career_result"]
        
        st.markdown(f"""
        <div class="raised-card">
            <h3 style="margin-top:0; color:#1b4332;">🌐 {res.get('industry', industry)} - 行业全景综述</h3>
            <p style="font-size: 15px; line-height: 1.6; color: #2d6a4f;">{res.get('overview', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        positions = res.get('positions', [])
        all_cities = set()
        for pos in positions:
            for c in pos.get('big_tech_companies', []) + pos.get('boutique_companies', []):
                if c.get('city'):
                    all_cities.add(c.get('city'))
        
        selected_city = "全部城市"
        if all_cities:
            city_list = ["全部城市"] + sorted(list(all_cities))
            selected_city = st.selectbox("📍 按工作城市过滤招聘企业：", city_list)

        st.markdown("### 💼 核心岗位矩阵与企业直推清单")
        for pos in positions:
            p_title = pos.get('title')
            with st.container():
                st.markdown(f"""
                <div class="raised-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #1b4332;">📌 {p_title}</h3>
                        <span style="background: #d8f3dc; color: #2d6a4f; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 13px;">
                            薪资: {pos.get('salary_level', '面议')}
                        </span>
                    </div>
                    <p style="margin-top: 10px; color: #40916c; font-size: 14px;"><strong>岗位职责与痛点：</strong>{pos.get('description')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("推荐指数", f"{pos.get('recommendation', {}).get('score', '90')}分")
                m2.metric("求职难度", pos.get('difficulty', '中'))
                m3.metric("市场需求", pos.get('market_demand', '旺盛'))
                st.write(f"**核心商业场景**: {pos.get('business')}")
                
                # 修复联动：精准传递当前点击的岗位名称
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"🔍 深度解构【{p_title}】并查看面试考点", key=f"jump_pos_{p_title}", use_container_width=True):
                        st.session_state.target_position = p_title
                        st.session_state.current_page = "岗位深度解析"
                        st.rerun()
                with col_btn2:
                    if st.button(f"🏢 查看【{p_title}】相关公司招聘情报", key=f"jump_comp_for_{p_title}", use_container_width=True):
                        # 默认取该岗位下第一家大厂或公司作为目标公司带入情报站
                        first_comp = "OpenAI"
                        if pos.get('big_tech_companies'):
                            first_comp = pos.get('big_tech_companies')[0].get('name')
                        elif pos.get('boutique_companies'):
                            first_comp = pos.get('boutique_companies')[0].get('name')
                        st.session_state.target_company = first_comp
                        st.session_state.target_position = p_title
                        st.session_state.current_page = "公司情报站"
                        st.rerun()

                col_big, col_boutique = st.columns(2)
                
                with col_big:
                    st.markdown("#### 🏛️ 公认行业大厂")
                    big_comps = [c for c in pos.get('big_tech_companies', []) if selected_city == "全部城市" or c.get('city') == selected_city]
                    if not big_comps:
                        st.caption("该城市暂无大厂直推记录。")
                    else:
                        for comp in big_comps:
                            c_name = comp.get('name')
                            hiring_html = '<span class="hiring-badge"><span class="green-dot"></span>正在热招</span>' if comp.get('is_hiring', True) else ''
                            st.markdown(f"""
                            <div style="background: #f8faf9; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2ece6;">
                                <div style="font-weight: 600; color: #1b4332;">{c_name} <span style="font-size:12px; color:#666;">({comp.get('city', '')})</span> {hiring_html}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            bc1, bc2, bc3 = st.columns(3)
                            if comp.get('official_url'):
                                bc1.link_button("🌐 官网", comp.get('official_url'), use_container_width=True)
                            if comp.get('linkedin_url'):
                                bc2.link_button("🔗 LinkedIn", comp.get('linkedin_url'), use_container_width=True)
                            if bc3.button("📋 查情报", key=f"btn_comp_{c_name}_{p_title}", use_container_width=True):
                                st.session_state.target_company = c_name
                                st.session_state.target_position = p_title
                                st.session_state.current_page = "公司情报站"
                                st.rerun()

                with col_boutique:
                    st.markdown("#### 💎 小而美 / 高成长创新企业")
                    bout_comps = [c for c in pos.get('boutique_companies', []) if selected_city == "全部城市" or c.get('city') == selected_city]
                    if not bout_comps:
                        st.caption("该城市暂无小而美企业直推记录。")
                    else:
                        for comp in bout_comps:
                            c_name = comp.get('name')
                            hiring_html = '<span class="hiring-badge"><span class="green-dot"></span>正在热招</span>' if comp.get('is_hiring', True) else ''
                            st.markdown(f"""
                            <div style="background: #f8faf9; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2ece6;">
                                <div style="font-weight: 600; color: #1b4332;">{c_name} <span style="font-size:12px; color:#666;">({comp.get('city', '')})</span> {hiring_html}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            cc1, cc2, cc3 = st.columns(3)
                            if comp.get('official_url'):
                                cc1.link_button("🌐 官网", comp.get('official_url'), use_container_width=True)
                            if comp.get('linkedin_url'):
                                cc2.link_button("🔗 LinkedIn", comp.get('linkedin_url'), use_container_width=True)
                            if cc3.button("📋 查情报", key=f"btn_boutique_{c_name}_{p_title}", use_container_width=True):
                                st.session_state.target_company = c_name
                                st.session_state.target_position = p_title
                                st.session_state.current_page = "公司情报站"
                                st.rerun()
                st.markdown("---")

# ---------------- 2. 职业生态树 (精准传递选中岗位) ----------------
elif page == "职业生态树":
    st.markdown("## 🌳 矩阵化职业生态树")
    st.markdown("<p style='color: #52796f;'>点击任意细分岗位卡片，系统将自动无缝跳转至该岗位的【深度解析】模块！</p>", unsafe_allow_html=True)
    
    industry = st.text_input("请输入要解构的行业生态：", "人工智能与大模型产业")
    if st.button("构建生态树", type="primary"):
        with st.spinner("AI 正在构建多维职业生态树..."):
            res = ai.explore_tree(industry)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("生态树生成完毕！")
                st.session_state["last_tree_result"] = res

    if "last_tree_result" in st.session_state:
        res = st.session_state["last_tree_result"]
        if isinstance(res, dict):
            for category, job_list in res.items():
                st.markdown(f"""
                <div class="raised-card">
                    <h3 style="color: #1b4332; border-bottom: 2px solid #d8f3dc; padding-bottom: 8px;">📂 {category}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if isinstance(job_list, list) and job_list:
                    cols = st.columns(min(len(job_list), 3))
                    for idx, job in enumerate(job_list):
                        with cols[idx % len(cols)]:
                            st.markdown(f"""
                            <div style="background: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #2d6a4f; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 10px;">
                                <div style="font-weight: 600; color: #1b4332; margin-bottom: 8px;">🌿 {job}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"🎯 深度解析此岗位", key=f"tree_jump_{category}_{idx}", use_container_width=True):
                                st.session_state.target_position = job
                                st.session_state.current_page = "岗位深度解析"
                                st.rerun()

# ---------------- 3. 岗位深度解析 ----------------
elif page == "岗位深度解析":
    st.markdown("## 🎯 岗位深度硬核解析")
    
    default_pos = st.session_state.get("target_position", "大模型产品经理")
    pos_name = st.text_input("请输入或确认要深度解构的岗位名称：", value=default_pos)
    
    if st.button("开始深度剖析与面试考点拆解", type="primary") or pos_name:
        with st.spinner(f"AI 正在深度剖析【{pos_name}】的底层逻辑、技术栈与高频面试真题..."):
            res = ai.position_detail(pos_name)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("解析完成！")
                st.markdown(f"""
                <div class="raised-card">
                    <h2 style="color: #1b4332; margin-top:0;">📋 岗位：{res.get('title', pos_name)}</h2>
                    <p style="font-size: 16px; color: #2d6a4f; font-weight: 500;">{res.get('overview', '')}</p>
                    <p><strong>💰 薪资评估：</strong>{res.get('salary_range', '')}</p>
                    <p><strong>📈 晋升成长路径：</strong>{res.get('growth_path', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown("""
                    <div class="raised-card">
                        <h4 style="color:#1b4332;">🛠️ 核心硬技能栈</h4>
                    """, unsafe_allow_html=True)
                    for tech in res.get('tech_stack', []):
                        st.markdown(f"- ✅ {tech}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="raised-card">
                        <h4 style="color:#1b4332;">📝 典型日常工作流</h4>
                    """, unsafe_allow_html=True)
                    for wf in res.get('workflow', []):
                        st.markdown(f"- 📌 {wf}")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_d2:
                    st.markdown("""
                    <div class="raised-card">
                        <h4 style="color:#1b4332;">🚀 核心职责拆解</h4>
                    """, unsafe_allow_html=True)
                    for resp in res.get('responsibilities', []):
                        st.markdown(f"- 🔹 {resp}")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("""
                    <div class="raised-card">
                        <h4 style="color:#1b4332;">💡 高频硬核面试考点与解题思路</h4>
                    """, unsafe_allow_html=True)
                    for idx, tip in enumerate(res.get('interview_tips', []), 1):
                        st.markdown(f"""
                        <div style="background: #f0f7f4; padding: 10px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #40916c;">
                            <strong>考点 {idx}:</strong> {tip}
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # 联动按钮：跳转至公司情报站并带入当前岗位
                if st.button(f"🏢 查看哪些公司正在热招【{pos_name}】", type="secondary"):
                    st.session_state.target_position = pos_name
                    st.session_state.current_page = "公司情报站"
                    st.rerun()

# ---------------- 4. 公司情报站 (精准响应用户选择的岗位和公司) ----------------
elif page == "公司情报站":
    st.markdown("## 🏢 公司情报站与实时职位库")
    
    default_comp = st.session_state.get("target_company", "OpenAI")
    default_pos = st.session_state.get("target_position", "")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        company_name = st.text_input("请输入目标公司名称：", value=default_comp)
    with col_c2:
        filter_pos = st.text_input("关联聚焦的岗位（可选）：", value=default_pos)
    
    if st.button("获取深度公司情报", type="primary") or company_name:
        with st.spinner(f"AI 正在搜集【{company_name}】针对【{filter_pos if filter_pos else '全岗位'}】的组织架构与招聘情报..."):
            res = ai.company_detail(company_name, filter_pos)
            if "error" in res:
                st.error(f"调用出错: {res['error']}")
            else:
                st.success("情报获取成功！")
                st.markdown(f"""
                <div class="raised-card">
                    <h2 style="color: #1b4332; margin-top:0;">🏢 {res.get('name', company_name)}</h2>
                    <p style="font-size: 15px; color: #2d6a4f;">{res.get('intro', '')}</p>
                    <p><strong>💰 薪资福利与期权：</strong>{res.get('salary_benefits', '')}</p>
                    <p><strong>🎯 面试风格与轮次：</strong>{res.get('interview_experience', '')}</p>
                    <p><strong>💬 员工真实评价：</strong>{res.get('employee_review', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"### 📋 {company_name} 当前热招职位明细清单")
                open_pos = res.get('open_positions_with_details', [])
                if not open_pos:
                    st.info("暂无具体的抓取职位明细。")
                else:
                    for op in open_pos:
                        op_title = op.get('position_title')
                        st.markdown(f"""
                        <div class="raised-card" style="padding: 15px;">
                            <div style="display: flex; justify-content: space-between;">
                                <h4 style="margin: 0; color: #1b4332;">🔥 {op_title}</h4>
                                <span class="hiring-badge"><span class="green-dot"></span>急招</span>
                            </div>
                            <p style="margin: 6px 0; color: #52796f; font-size: 14px;"><strong>所属部门:</strong> {op.get('department')}</p>
                            <p style="margin: 0; color: #2d6a4f; font-size: 14px;"><strong>核心要求:</strong> {op.get('requirements')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"🎯 联动解析【{op_title}】岗位", key=f"comp_jump_{op_title}"):
                            st.session_state.target_position = op_title
                            st.session_state.current_page = "岗位深度解析"
                            st.rerun()

# ---------------- 5. JD 简历优化 (专注 ATS 机器过筛) ----------------
elif page == "JD 简历优化":
    st.markdown("## 📝 ATS 简历机器过筛与优化")
    st.markdown("<p style='color: #52796f;'>粘贴目标 JD，系统将自动逆向解析 ATS（Applicant Tracking System）机器筛选的硬核过筛关键词，助你第一步突破机审！</p>", unsafe_allow_html=True)
    
    jd_text = st.text_area("请粘贴目标岗位的 JD（招聘要求）原文：", height=200, placeholder="在此粘贴招聘 JD 原文...")
    if st.button("开始 ATS 机器过筛诊断", type="primary"):
        if not jd_text.strip():
            st.warning("请先输入有效的 JD 内容！")
        else:
            with st.spinner("AI 正在逆向拆解 ATS 机器过滤规则与高频硬核关键词..."):
                res = ai.jd_analysis(jd_text)
                if "error" in res:
                    st.error(f"调用出错: {res['error']}")
                else:
                    st.success("ATS 诊断完成！")
                    
                    # ATS 关键词展示区
                    st.markdown("""
                    <div class="raised-card" style="border-left: 6px solid #2e7d32;">
                        <h3 style="color:#1b4332; margin-top:0;">🛡️ ATS 机器过筛必须包含的硬核关键词</h3>
                        <p style="color:#52796f; font-size:14px;">请确保以下高频关键词在你的简历中完整出现（建议原文原样匹配，避免机器解析失败）：</p>
                    """, unsafe_allow_html=True)
                    ats_keywords = res.get('ats_keywords_must_have', [])
                    keywords_html = "".join([f"<span style='background:#d8f3dc; color:#1b4332; padding:6px 12px; border-radius:6px; margin-right:8px; display:inline-block; margin-bottom:8px; font-weight:600; border: 1px solid #b7e4c7;'>🔑 {kw}</span>" for kw in ats_keywords])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 简历包装建议区
                    st.markdown("""
                    <div class="raised-card">
                        <h3 style="color:#1b4332;">📈 针对 ATS 系统的简历排版与包装建议</h3>
                    """, unsafe_allow_html=True)
                    for tip in res.get('resume_writing_tips', []):
                        st.markdown(f"- ✨ {tip}")
                    st.markdown("</div>", unsafe_allow_html=True)