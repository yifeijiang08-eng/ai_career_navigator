import os
import json
from openai import OpenAI

class AIService:
    def __init__(self):
        # 从 Streamlit Secrets 中读取腾讯混元 API Key
        self.api_key = os.environ.get("HUNYUAN_API_KEY") or os.environ.get("TENCENT_API_KEY") or ""
        self.base_url = "https://api.hunyuan.cloud.tencent.com/v1" # 腾讯混元兼容 OpenAI 的 endpoint
        
        if not self.api_key:
            self.client = None
        else:
            # 使用 OpenAI 客户端对接混元
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
        # 腾讯混元主力大模型名称（可根据需要调整，如 hunyuan-pro 或 hunyuan-standard）
        self.model_name = "Hy3"

    def _call_gemini_json(self, prompt: str) -> dict:
        """调用腾讯混元并强制输出标准 JSON 格式"""
        if not self.client:
            return {"error": "未检测到有效的 HUNYUAN_API_KEY，请检查 Streamlit Cloud 的 Secrets 设置！"}
            
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个严谨的求职与职业规划专家，必须严格只输出符合要求的 JSON 格式，不要包含任何多余的markdown标记或前后缀说明。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"} # 强制 JSON 输出
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def career_nav(self, industry: str) -> dict:
        prompt = f"""
        请为【{industry}】这个行业生成一份详尽的求职全景导航。
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