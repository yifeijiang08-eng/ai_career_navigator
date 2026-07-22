import os
import json
from google import genai
from google.genai import types

class AIService:
    def __init__(self):
        # 从 Streamlit Secrets 或系统环境变量中安全读取 API Key
        self.api_key = (
            os.environ.get("GEMINI_API_KEY") or 
            os.environ.get("GOOGLE_API_KEY") or 
            ""
        )
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash"
        # 调试日志：可以在 Streamlit 后台看到是否成功读到了 Key
        if not self.api_key:
            print("❌ 警告：未检测到 GEMINI_API_KEY，请检查 Streamlit Secrets 设置！")
        else:
            print("✅ 成功：已加载 Gemini API Key")

        # 初始化 Google GenAI 客户端
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash"

    def _call_gemini_json(self, prompt: str) -> dict:
        """通用私有方法：调用 Gemini 并强制输出标准 JSON 格式"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}

    def career_nav(self, industry: str) -> dict:
        prompt = f"""
        你是一个顶级的职业规划与AI求职专家。请为【{industry}】这个行业生成一份详尽的求职全景导航。
        必须严格输出以下 JSON 结构：
        {{
            "industry": "{industry}",
            "overview": "行业发展现状与趋势概览（50字左右）",
            "positions": [
                {{
                    "title": "岗位名称",
                    "description": "岗位职责简述",
                    "recommendation": {{"score": "95"}},
                    "difficulty": "高/中/低",
                    "market_demand": "火爆/平稳",
                    "salary_level": "薪资范围",
                    "business": "涉及的核心业务场景"
                }}
            ],
            "keywords": {{
                "cn": ["中文搜索关键词1", "关键词2"],
                "en": ["English Keyword 1", "Keyword 2"]
            }}
        }}
        """
        return self._call_gemini_json(prompt)

    def explore_tree(self, industry: str) -> dict:
        prompt = f"""
        请为【{industry}】行业设计一个多维度的矩阵化职业生态树。
        按不同的技术或业务方向分类（例如：研发类、产品类、运营类等）。
        必须严格输出 JSON 格式，形如：
        {{
            "研发与技术方向": ["岗位A", "岗位B"],
            "产品与商业方向": ["岗位C", "岗位D"]
        }}
        """
        return self._call_gemini_json(prompt)

    def position_detail(self, position: str) -> dict:
        prompt = f"""
        请对【{position}】这个岗位进行深度解析。
        必须严格输出以下 JSON 结构：
        {{
            "title": "{position}",
            "overview": "岗位一句话总结",
            "salary_range": "年薪或月薪范围",
            "growth_path": "晋升成长路径",
            "responsibilities": ["职责1", "职责2"],
            "workflow": ["日常工作步骤1", "步骤2"],
            "tech_stack": ["技术1", "技术2"],
            "recommended_projects": ["练手项目1", "项目2"],
            "interview_tips": ["面试考点1", "面试考点2"]
        }}
        """
        return self._call_gemini_json(prompt)

    def company_detail(self, company: str) -> dict:
        prompt = f"""
        请提供【{company}】这家公司的求职情报与内幕。
        必须严格输出 JSON 结构：
        {{
            "name": "{company}",
            "intro": "公司简介",
            "salary_benefits": "薪资福利特点",
            "cities": ["主要办公城市1", "城市2"],
            "hiring_channels": ["官方招聘网址或渠道1"],
            "open_positions": ["热招岗位1", "岗位2"],
            "interview_experience": "面试风格特点",
            "employee_review": "职场评价"
        }}
        """
        return self._call_gemini_json(prompt)

    def jd_analysis(self, jd_text: str) -> dict:
        prompt = f"""
        请分析以下招聘 JD 原文，并给出高频技能与简历优化指南：
        {jd_text}
        必须严格输出 JSON 结构：
        {{
            "job_title": "识别出的岗位名称",
            "core_competencies": ["核心能力1", "能力2"],
            "high_frequency_skills": ["技能1", "技能2"],
            "resume_writing_tips": ["包装建议1", "建议2"],
            "interview_questions": ["可能被问的高频面试题1", "问题2"]
        }}
        """
        return self._call_gemini_json(prompt)