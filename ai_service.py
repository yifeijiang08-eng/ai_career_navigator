import json
import os
import streamlit as st
from openai import OpenAI
from prompts.career import CAREER_NAVIGATOR_PROMPT, EXPLORE_TREE_PROMPT
from prompts.position import POSITION_DETAIL_PROMPT
from prompts.company import COMPANY_DETAIL_PROMPT

class AIService:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "你的-API-Key")
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _call_llm(self, system_prompt: str, user_input: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices.message.content)
        except Exception as e:
            return {"error": str(e)}

    def career_nav(_self, industry: str) -> dict:
        return self._call_llm(CAREER_NAVIGATOR_PROMPT, f"行业方向：{industry}")

    def explore_tree(_self, industry: str) -> dict:
        return self._call_llm(EXPLORE_TREE_PROMPT, f"行业方向：{industry}")

    def position_detail(_self, position_name: str) -> dict:
        return self._call_llm(POSITION_DETAIL_PROMPT, f"目标岗位：{position_name}")

    def company_detail(_sself, company_name: str) -> dict:
        return self._call_llm(COMPANY_DETAIL_PROMPT, f"目标公司：{company_name}")
    import json
import os
import streamlit as st
from openai import OpenAI
from prompts.career import CAREER_NAVIGATOR_PROMPT, EXPLORE_TREE_PROMPT
from prompts.position import POSITION_DETAIL_PROMPT
from prompts.company import COMPANY_DETAIL_PROMPT
from prompts.jd import JD_ANALYSIS_PROMPT

class AIService:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _call_llm(self, system_prompt: str, user_input: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices.message.content)
        except Exception as e:
            return {"error": str(e)}

    def career_nav(_self, industry: str) -> dict:
        return self._call_llm(CAREER_NAVIGATOR_PROMPT, f"行业方向：{industry}")

    def explore_tree(_self, industry: str) -> dict:
        return self._call_llm(EXPLORE_TREE_PROMPT, f"行业方向：{industry}")

    def position_detail(_self, position_name: str) -> dict:
        return self._call_llm(POSITION_DETAIL_PROMPT, f"目标岗位：{position_name}")

    def company_detail(_self, company_name: str) -> dict:
        return self._call_llm(COMPANY_DETAIL_PROMPT, f"目标公司：{company_name}")

    def jd_analysis(_self, jd_text_or_position: str) -> dict:
        return self._call_llm(JD_ANALYSIS_PROMPT, f"分析对象（JD内容或岗位名称）：{jd_text_or_position}") 