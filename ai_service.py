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
                    {"role": "system", "content": "你是一个资深的全球科技与人工智能行业猎头、职业规划专家。你必须输出极度详尽、深度、包含大量行业干货和真实现状的 JSON 格式数据。严禁套话空话。"},
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

    def company_detail(self, company: str) -> dict:
        prompt = f"""
        请提供【{company}】这家公司的深度求职情报。
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
                }},
                {{
                    "position_title": "热招岗位名称2",
                    "department": "所属部门",
                    "requirements": "核心硬性要求"
                }}
            ],
            "interview_experience": "面试风格、轮次与高频风格特点",
            "employee_review": "真实工作体验与发展评价"
        }}
        """
        return self._call_gemini_json(prompt)

    def jd_analysis(self, jd_text: str) -> dict:
        prompt = f"""
        请深度分析以下招聘 JD 原文，并给出精准的技能拆解与简历优化指南：
        {jd_text}
        必须严格输出 JSON 结构：
        {{
            "job_title": "识别出的岗位名称",
            "core_competencies": ["核心能力1", "能力2"],
            "high_frequency_skills": ["技能1", "技能2"],
            "resume_writing_tips": ["极具含金量的包装建议1", "建议2"],
            "interview_questions": ["可能被问的犀利面试题1", "问题2"]
        }}
        """
        return self._call_gemini_json(prompt)