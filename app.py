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
    st.session_state.target_company = "微软 (Microsoft)"

# ================= 侧边栏导航菜单 =================
with st.sidebar:
    st.markdown("### 🧭 导航菜单")
    st.markdown("<p style='font-size: 13px; color: #52796f;'>多维联动求职系统</p>", unsafe_allow_html=True)
    
    nav_items = [
        ("📈 行业全景导航", "行业全景导航"),
        ("🌳 职业生态树", "职业生态树"),
        ("🎯 岗位深度解析", "岗位深度解析"),
        ("🏢 公司情报站", "公司情报站"),
        ("📝 HRD 简历特训与优化", "JD 简历优化")
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
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"🔍 深度解构【{p_title}】并查看面试考点", key=f"jump_pos_{p_title}", use_container_width=True):
                        st.session_state.target_position = p_title
                        st.session_state.current_page = "岗位深度解析"
                        st.rerun()
                with col_btn2:
                    if st.button(f"🏢 查看【{p_title}】相关公司招聘情报", key=f"jump_comp_for_{p_title}", use_container_width=True):
                        first_comp = "微软 (Microsoft)"
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

# ---------------- 2. 职业生态树 ----------------
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
    st.markdown("## 🎯 岗位深度硬核解析与性格匹配（MBTI/E-I人）")
    
    default_pos = st.session_state.get("target_position", "大模型产品经理")
    pos_name = st.text_input("请输入或确认要深度解构的岗位名称：", value=default_pos)
    
    if st.button("开始深度剖析与性格特点拆解", type="primary") or pos_name:
        with st.spinner(f"AI 正在深度剖析【{pos_name}】的技术栈、日常工作流与 MBTI 性格匹配倾向..."):
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
                        <h4 style="color:#1b4332;">👥 沟通特点与 MBTI 性格倾向（E人/I人适配）</h4>
                    """, unsafe_allow_html=True)
                    for comm in res.get('communication_and_mbti', []):
                        st.markdown(f"- 💡 {comm}")
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

                if st.button(f"🏢 查看哪些公司正在热招【{pos_name}】", type="secondary"):
                    st.session_state.target_position = pos_name
                    st.session_state.current_page = "公司情报站"
                    st.rerun()

# ---------------- 4. 公司情报站 ----------------
elif page == "公司情报站":
    st.markdown("## 🏢 公司情报站与多维评分雷达（环境、福利、加班、假期）")
    
    # 彻底修复：使用独立的 Session State 变量，防止输入框死锁在固定值
    if "input_company_name" not in st.session_state:
        st.session_state.input_company_name = st.session_state.get("target_company", "微软 (Microsoft)")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        company_name = st.text_input("请输入目标公司名称：", key="input_company_name")
    with col_c2:
        filter_pos = st.text_input("关联聚焦的岗位（可选）：", value=st.session_state.get("target_position", ""))
    
    if st.button("获取深度公司情报与多维评分", type="primary") or company_name:
        with st.spinner(f"AI 正在独立搜集【{company_name}】针对【{filter_pos if filter_pos else '全岗位'}】的真实环境、福利及热招职位..."):
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
                
                # 公司多维评分面板
                st.markdown("""
                <div class="raised-card" style="background: #fafdfb;">
                    <h3 style="color:#1b4332; margin-top:0;">📊 公司多维体验综合评分面板</h3>
                """, unsafe_allow_html=True)
                c_scores = res.get('company_scores', {})
                cs1, cs2, cs3, cs4 = st.columns(4)
                cs1.metric("内部办公环境", f"{c_scores.get('internal_environment', 85)}分")
                cs2.metric("薪酬福利水平", f"{c_scores.get('benefits_score', 88)}分")
                cs3.metric("工作强度/少加班度", f"{c_scores.get('overtime_score', 75)}分")
                cs4.metric("假期制度丰富度", f"{c_scores.get('holiday_score', 80)}分")
                st.markdown("</div>", unsafe_allow_html=True)
                
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

# ---------------- 5. HRD 简历特训与高级优化 ----------------
elif page == "JD 简历优化":
    st.markdown("## 📝 HRD 简历特训与全维度高分优化")
    st.markdown("<p style='color: #52796f;'>请先选择你要申请的职位、公司及工作地点，系统将精准定位申请要求、拆解 JD、对照简历并给出多维打分、HRD 级润色、量化旁侧批注及面试官追问！</p>", unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        target_pos_input = st.text_input("🎯 目标职位：", value=st.session_state.get("target_position", "大模型产品经理"))
    with col_s2:
        target_comp_input = st.text_input("🏢 目标公司：", value=st.session_state.get("target_company", "微软 (Microsoft)"))
    with col_s3:
        target_loc_input = st.text_input("📍 工作地点：", value="北京 / 远程")
        
    jd_text = st.text_area("📋 请粘贴目标岗位的 JD（招聘要求）原文：", height=150, placeholder="在此粘贴招聘 JD 原文...")
    user_resume = st.text_area("📄 请粘贴你目前的原始简历内容：", height=200, placeholder="在此粘贴你的工作经历、项目经历等原始简历文本...")
    
    if st.button("🚀 开始 HRD 级深度对标与面试全维特训", type="primary"):
        if not jd_text.strip() or not user_resume.strip():
            st.warning("请完整填写 JD 原文和你的原始简历内容！")
        else:
            with st.spinner("资深 HRD 正在进行申请表分析、六维评分、量化批注、面试追问与能力信号评估..."):
                res = ai.advanced_resume_analysis(target_pos_input, target_comp_input, target_loc_input, jd_text, user_resume)
                if "error" in res:
                    st.error(f"调用出错: {res['error']}")
                else:
                    st.success("HRD 级简历诊断与面试特训完成！")
                    
                    # 1. 招聘经理信号灯评估
                    st.markdown("""
                    <div class="raised-card" style="border-left: 6px solid #2e7d32; background: #fafdfb;">
                        <h3 style="color:#1b4332; margin-top:0;">🚦 招聘经理（Hiring Manager）第一印象信号灯</h3>
                    """, unsafe_allow_html=True)
                    hm_signals = res.get('hiring_manager_signals', {})
                    st.write("**🟢 前三个最强能力信号：**")
                    for sig in hm_signals.get('strong_signals', []):
                        st.markdown(f"- ✅ {sig}")
                    st.write("**🔴 最弱的能力信号 / 防御红线（需在面试中重点弥补）：**")
                    st.markdown(f"- ⚠️ {hm_signals.get('weak_signal', '')}")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # 2. 申请表要求与 JD 拆解
                    st.markdown("""
                    <div class="raised-card">
                        <h3 style="color:#1b4332; margin-top:0;">📌 申请表必备材料与 JD 核心拆解</h3>
                    """, unsafe_allow_html=True)
                    st.write("**申请表/底层信息项预测：**")
                    for req in res.get('position_application_requirements', []):
                        st.markdown(f"- 📋 {req}")
                        
                    st.write("**JD 核心要求：**")
                    core_bk = res.get('jd_core_breakdown', {})
                    st.markdown(f"- **核心职责：** {', '.join(core_bk.get('core_responsibilities', []))}")
                    st.markdown(f"- **关键技能：** {', '.join(core_bk.get('key_skills', []))}")
                    st.markdown(f"- **经验要求：** {', '.join(core_bk.get('experience_requirements', []))}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 3. 六维评分面板
                    st.markdown("""
                    <div class="raised-card">
                        <h3 style="color:#1b4332; margin-top:0;">📊 简历多维度综合评分面板</h3>
                    """, unsafe_allow_html=True)
                    scores = res.get('scores', {})
                    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
                    sc1.metric("JD 匹配度", f"{scores.get('jd_matching', 80)}分")
                    sc2.metric("量化成果", f"{scores.get('quantified_achievements', 60)}分")
                    sc3.metric("结构逻辑", f"{scores.get('structural_logic', 75)}分")
                    sc4.metric("语言专业度", f"{scores.get('language_professionalism', 70)}分")
                    sc5.metric("排版规范", f"{scores.get('formatting', 80)}分")
                    sc6.metric("ATS 友好度", f"{scores.get('ats_friendliness', 75)}分")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 4. HRD 总监总体点评
                    st.markdown(f"""
                    <div class="raised-card" style="background: #f0f7f4;">
                        <h3 style="color:#1b4332; margin-top:0;">💡 HRD 顾问深度总评</h3>
                        <p style="font-size: 15px; color: #2d6a4f; line-height: 1.6;">{res.get('hrd_consultant_review', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 5. 亮点强调 vs 补充不足
                    col_h1, col_h2 = st.columns(2)
                    with col_h1:
                        st.markdown("""
                        <div class="raised-card">
                            <h4 style="color:#1b4332;">✨ 高度匹配需重点强调的部分</h4>
                        """, unsafe_allow_html=True)
                        for item in res.get('matching_parts_to_highlight', []):
                            st.markdown(f"- 🟢 {item}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with col_h2:
                        st.markdown("""
                        <div class="raised-card">
                            <h4 style="color:#1b4332;">⚠️ 描述不足需补充完善的部分</h4>
                        """, unsafe_allow_html=True)
                        for item in res.get('insufficient_parts_to_supplement', []):
                            st.markdown(f"- 🟡 {item}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    # 6. 工作经历 / 项目经验高级润色（含量化旁侧批注）
                    st.markdown("""
                    <div class="raised-card">
                        <h3 style="color:#1b4332; margin-top:0;">✍️ 工作经历 HRD 级高级润色与量化防穿帮旁侧批注</h3>
                        <p style="color: #52796f; font-size: 14px;">润色后话术已将动词升级并加入量化指标，下方附带<strong>面试官追问防穿帮批注</strong>：</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for idx, exp in enumerate(res.get('enhanced_experience_bullets', []), 1):
                        st.markdown(f"""
                        <div class="raised-card" style="background: #fcfdfc; border-left: 4px solid #40916c;">
                            <p style="color: #666; font-size: 13px; margin-bottom: 4px;"><strong>原话术片段 {idx}：** {exp.get('original_snippet')}</p>
                            <p style="color: #1b4332; font-size: 15px; font-weight: 600; margin-top: 8px;"><strong>🔥 润色后话术（高亮标注）：</strong></p>
                            <p style="background: #e8f5e9; padding: 10px; border-radius: 6px; color: #2e7d32; font-size: 15px;">{exp.get('optimized_snippet')}</p>
                            <p style="color: #52796f; font-size: 13px; margin-top: 6px;"><strong>💡 顾问解析：</strong> {exp.get('reason_for_change')}</p>
                            <p style="background: #fff8e1; padding: 10px; border-radius: 6px; color: #b78103; font-size: 13px; margin-top: 8px; border: 1px solid #ffe0b2;"><strong>🛡️ 量化指标旁侧批注（面试如何解释）：</strong> {exp.get('quantified_side_note')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # 7. 面试官高频追问 5 题
                    st.markdown("""
                    <div class="raised-card" style="border-left: 6px solid #1b4332;">
                        <h3 style="color:#1b4332; margin-top:0;">🎤 面试官视角：看完你简历后最可能追问的 5 个灵魂考题</h3>
                        <p style="color: #52796f; font-size: 14px;">资深面试官在仔细审阅你的简历后，通常会针对这些潜在漏洞或亮点进行深挖：</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for idx, q_item in enumerate(res.get('interviewer_hard_questions', []), 1):
                        st.markdown(f"""
                        <div style="background: #f0f7f4; padding: 14px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #c8e6c9;">
                            <strong style="color: #1b4332; font-size: 15px;">追问 {idx}：{q_item.get('question')}</strong>
                            <p style="color: #2d6a4f; font-size: 13px; margin: 6px 0 0 0;"><strong>🎯 考察意图与解题思路：</strong> {q_item.get('intent')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    # 8. ATS 过筛关键词
                    st.markdown("""
                    <div class="raised-card" style="border-left: 6px solid #2e7d32;">
                        <h3 style="color:#1b4332; margin-top:0;">🛡️ ATS 机器过筛必须布局的核心关键词</h3>
                    """, unsafe_allow_html=True)
                    ats_kw = res.get('ats_keywords_must_have', [])
                    kw_html = "".join([f"<span style='background:#d8f3dc; color:#1b4332; padding:6px 12px; border-radius:6px; margin-right:8px; display:inline-block; margin-bottom:8px; font-weight:600; border: 1px solid #b7e4c7;'>🔑 {kw}</span>" for kw in ats_kw])
                    st.markdown(kw_html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)