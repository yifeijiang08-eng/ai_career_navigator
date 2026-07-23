import os
import json
from openai import OpenAI

class AIService:
    def __init__(self):
        self.api_key = os.environ.get("HUNYUAN_API_KEY") or os.environ.get("TENCENT_API_KEY") or ""
        self.base_url = "https://tokenhub.tencentmaas.com/v1"
        
        if not self.api_key:
            self.client = None
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
        self.model_name = "hy3"

    def _call_gemini_json(self, prompt: str) -> dict:
        if not self.client:
            return {"error": "未检测到有效的 HUNYUAN_API_KEY，请检查 Streamlit Cloud 的 Secrets 设置！"}
            
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个资深的全球 500 强企业人力资源总监（HRD）、技术合伙人兼顶级职业发展顾问。你精通 ATS 机器筛选机制与候选人包装，擅长将平淡的简历润色为极具说服力、量化成果且高大上的专业履历。必须输出严格的 JSON 格式数据。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def career_nav(self, industry: str, cross_skill: str = "") -> dict:
        cross_desc = f"，同时重点结合用户的跨界背景/技能【{cross_skill}】来挖掘独特的切入机会" if cross_skill else ""
        prompt = f"""
        请为【{industry}】行业生成一份极其详尽、兼具宏观与微观的求职全景导航{cross_desc}。
        必须严格输出以下 JSON 结构：
        {{
            "industry": "{industry}",
            "overview": "行业发展现状、资本热度与未来3年趋势深度剖析（150字左右）",
            "positions": [
                {{
                    "title": "具体岗位名称",
                    "description": "极具深度的岗位职责与核心痛点剖析（100字以上）",
                    "recommendation": {{"score": "95"}},
                    "difficulty": "高/中/低",
                    "market_demand": "火爆/平稳",
                    "salary_level": "薪资范围（含期权/本地化薪资）",
                    "business": "涉及的核心业务场景与商业化落地路径",
                    "big_tech_companies": [
                        {{
                            "name": "公认大厂名称",
                            "city": "城市（如 慕尼黑/柏林/北京/旧金山）",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }}
                    ],
                    "boutique_companies": [
                        {{
                            "name": "小而美/高成长创新公司名称",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }}
                    ]
                }}
            ]
        }}
        """
        return self._call_gemini_json(prompt)

    def explore_tree(self, industry: str) -> dict:
        prompt = f"""
        请为【{industry}】行业设计一个多维度、细颗粒度的矩阵化职业生态树，包含各个细分方向及其具体岗位。
        必须严格输出 JSON 格式，形如：
        {{
            "核心研发与算法方向": ["大模型算法专家", "多模态研究员", "AI Infra 工程师"],
            "产品与商业化方向": ["AI产品经理", "海外商业化总监", "解决方案架构师"],
            "跨界融合与生态方向": ["AI伦理与合规专家", "小语种AI内容主编", "大模型数据运营专家"]
        }}
        """
        return self._call_gemini_json(prompt)

    def position_detail(self, position: str) -> dict:
        prompt = f"""
        请对【{position}】这个岗位进行极度深度、干货满满的硬核解析。
        必须严格输出以下 JSON 结构：
        {{
            "title": "{position}",
            "overview": "该岗位在当前技术浪潮中的战略定位与核心价值",
            "salary_range": "全球/国内薪资水平评估",
            "growth_path": "从初级到架构师/总监的完整晋升成长路径",
            "responsibilities": ["硬核职责1（含具体工作目标）", "职责2", "职责3"],
            "workflow": ["日常工作步骤1", "步骤2", "步骤3"],
            "tech_stack": ["必备硬技能1", "技能2", "技能3"],
            "recommended_projects": ["具备行业含金量的实战练手项目1", "项目2"],
            "interview_tips": [
                "高频硬核面试考点1（附解题思路/考察意图）",
                "高频硬核面试考点2",
                "高频硬核面试考点3",
                "高频硬核面试考点4"
            ]
        }}
        """
        return self._call_gemini_json(prompt)

    def company_detail(self, company: str, target_position: str = "") -> dict:
        pos_filter = f"，并重点展示或匹配【{target_position}】该岗位的招聘与业务需求" if target_position else ""
        prompt = f"""
        请提供【{company}】这家公司的深度求职情报{pos_filter}。
        必须严格输出 JSON 结构：
        {{
            "name": "{company}",
            "intro": "公司背景、核心技术壁垒与团队规模",
            "salary_benefits": "薪资结构、期权政策与福利特点",
            "cities": ["主要办公城市1", "城市2"],
            "open_positions_with_details": [
                {{
                    "position_title": "热招岗位名称1",
                    "department": "所属部门",
                    "requirements": "核心硬性要求"
                }}
            ],
            "interview_experience": "面试风格、轮次与高频风格特点",
            "employee_review": "真实工作体验与发展评价"
        }}
        """
        return self._call_gemini_json(prompt)

    def advanced_resume_analysis(self, position: str, company: str, location: str, jd_text: str, user_resume: str) -> dict:
        prompt = f"""
        你是一位资深人力资源总监（HRD）兼顶级职业发展顾问。
        用户目标岗位：【{position}】
        目标公司：【{company}】
        工作地点：【{location}】
        
        请结合以下 JD 原文，以及用户上传的原始简历，进行全方位的深度对标、打分与高级润色。
        
        JD 原文：
        {jd_text}
        
        用户原始简历：
        {user_resume}
        
        必须严格输出以下 JSON 结构：
        {{
            "position_application_requirements": [
                "针对该岗位、公司及地点的申请表必备材料/底层信息项1",
                "必备材料2",
                "合规或背景要求3"
            ],
            "jd_core_breakdown": {{
                "core_responsibilities": ["核心职责拆解1", "职责2"],
                "key_skills": ["关键技能要求1", "技能2"],
                "experience_requirements": ["经验硬性要求1", "经验2"]
            }},
            "scores": {{
                "jd_matching": 85,
                "quantified_achievements": 60,
                "structural_logic": 75,
                "language_professionalism": 70,
                "formatting": 80,
                "ats_friendliness": 78
            }},
            "hrd_consultant_review": "以 HRD 顾问身份给出的总体犀利点评与破局建议（150字左右）",
            "matching_parts_to_highlight": [
                "简历中与 JD 高度契合、需重点加粗/靠前排布的亮点1",
                "亮点2"
            ],
            "insufficient_parts_to_supplement": [
                "与 JD 相关但描述不够充分、需用户补充具体数据或场景的部分1",
                "部分2"
            ],
            "enhanced_experience_bullets": [
                {{
                    "original_snippet": "原始工作经历中的平淡描述片段（例如：负责日常产品迭代和功能跟进）",
                    "optimized_snippet": "润色后的话术（运用高级力量感动词，如：主导、驱动、赋能、重构，并使用量化指标包装。被修改的关键词请用 **[修改后关键词]** 格式高亮标注）",
                    "reason_for_change": "这样修改的 HRD 视角解释与说服力说明"
                }}
            ],
            "ats_keywords_must_have": ["ATS过筛必备核心关键词1", "关键词2", "关键词3"]
        }}
        """
        return self._call_gemini_json(prompt)