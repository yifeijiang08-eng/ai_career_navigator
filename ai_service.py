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
                    {"role": "system", "content": "你是一个深谙应届生求职、校招、管培生培养及实习生晋升的资深校园招聘总监。请确保推荐岗位贴近刚毕业或在校生实际，且企业列表必须丰富（不少于5家）。必须输出严格的 JSON 格式数据。"},
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
        请为【{industry}】行业生成一份面向【应届毕业生、实习生及管培生】的求职全景导航{cross_desc}。
        注意：岗位必须贴近刚入门的职业情况（例如：管培生、初级研究员、助理产品经理、储备干部、实习生等）。
        对于每个岗位，推荐的【公认大厂】与【小而美/高成长创新公司】加起来必须达到【5家以上】。
        必须严格输出以下 JSON 结构：
        {{
            "industry": "{industry}",
            "overview": "面向应届生/实习生的行业发展现状与入行机会剖析（150字左右）",
            "positions": [
                {{
                    "title": "具体入门岗位名称（如：XX管培生 / AI实习生 / 储备经理）",
                    "description": "针对新人的岗位培养机制与职责解析（100字以上）",
                    "recommendation": {{"score": "95"}},
                    "difficulty": "高/中/低",
                    "market_demand": "火爆/平稳",
                    "salary_level": "实习日薪或应届生校招年薪范围",
                    "business": "涉及的核心业务场景与新人成长路径",
                    "big_tech_companies": [
                        {{
                            "name": "大厂名称1",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }},
                        {{
                            "name": "大厂名称2",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }},
                        {{
                            "name": "大厂名称3",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }}
                    ],
                    "boutique_companies": [
                        {{
                            "name": "高成长/中型公司名称1",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }},
                        {{
                            "name": "高成长/中型公司名称2",
                            "city": "城市",
                            "is_hiring": true,
                            "official_url": "https://www.example.com",
                            "linkedin_url": "https://www.linkedin.com/company/example"
                        }},
                        {{
                            "name": "高成长/中型公司名称3",
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
        请为【{industry}】行业设计一个面向应届生、实习生及管培生的多维度职业生态树。
        必须严格输出 JSON 格式，形如：
        {{
            "管培生与综合储备方向": ["运营管培生", "产品管培生", "销售储备干部"],
            "初级技术与研发方向": ["初级算法工程师(校招)", "AI开发实习生", "测试开发实习生"],
            "初级商务与职能方向": ["海外运营实习生", "人力资源管培生", "数据分析助理"]
        }}
        """
        return self._call_gemini_json(prompt)

    def position_detail(self, position: str) -> dict:
        prompt = f"""
        请对【{position}】这个面向应届生/实习生的岗位进行深度硬核解析。
        必须严格输出以下 JSON 结构：
        {{
            "title": "{position}",
            "overview": "该岗位对职场新人的价值与培养体系剖析",
            "salary_range": "校招薪资/实习生薪资水平评估",
            "growth_path": "从新人到独当一面的完整晋升路线",
            "responsibilities": ["核心基础职责1", "职责2", "职责3"],
            "workflow": ["日常工作步骤1", "步骤2", "步骤3"],
            "tech_stack": ["必备基础技能1", "技能2", "技能3"],
            "communication_and_mbti": [
                "新人性格沟通特点要求",
                "MBTI 倾向建议（例如：该岗位更适合 E人 还是 I人，各有什么优势与挑战）"
            ],
            "recommended_projects": ["适合写在简历上的校园/实战项目1", "项目2"],
            "interview_tips": [
                "校招/实习高频面试考点1（附应对技巧）",
                "高频面试考点2",
                "高频面试考点3"
            ]
        }}
        """
        return self._call_gemini_json(prompt)

    def company_detail(self, company: str, target_position: str = "") -> dict:
        pos_filter = f"，并重点展示针对【{target_position}】的校招、管培生或实习生项目" if target_position else ""
        prompt = f"""
        请提供【{company}】这家公司针对应届生、管培生及实习生的求职情报{pos_filter}。
        必须严格输出 JSON 结构：
        {{
            "name": "{company}",
            "intro": "公司背景、校招培养体系与新人氛围",
            "salary_benefits": "校招薪资、实习补贴、住房补贴与基础福利",
            "cities": ["主要办公城市1", "城市2"],
            "company_scores": {{
                "internal_environment": 88,
                "benefits_score": 90,
                "overtime_score": 75,
                "holiday_score": 85
            }},
            "open_positions_with_details": [
                {{
                    "position_title": "校招/实习岗位名称1",
                    "department": "所属部门/管培生轮岗部门",
                    "requirements": "对应届生/实习生的基础要求"
                }}
            ],
            "interview_experience": "校招面试风格、群面(AC面)特点与轮次",
            "employee_review": "往届管培生或实习生的真实工作体验与成长评价"
        }}
        """
        return self._call_gemini_json(prompt)

    def advanced_resume_analysis(self, position: str, company: str, location: str, jd_text: str, user_resume: str) -> dict:
        prompt = f"""
        你是一位资深校园招聘总监兼校招面试官。
        目标岗位：【{position}】（面向应届生/实习生/管培生）
        目标公司：【{company}】
        工作地点：【{location}】
        
        请结合以下 JD 原文，以及用户上传的原始简历（通常为在校生或应届生简历），进行全方位的深度对标、打分、高级润色以及面试官视角评估。
        
        JD 原文：
        {jd_text}
        
        用户原始简历：
        {user_resume}
        
        必须严格输出以下 JSON 结构：
        {{
            "position_application_requirements": [
                "针对该校招/实习岗位的网申必备材料项1",
                "必备材料2"
            ],
            "jd_core_breakdown": {{
                "core_responsibilities": ["核心职责拆解1", "职责2"],
                "key_skills": ["关键技能要求1", "技能2"],
                "experience_requirements": ["校园经历/实习硬性要求1", "经验2"]
            }},
            "scores": {{
                "jd_matching": 85,
                "quantified_achievements": 60,
                "structural_logic": 75,
                "language_professionalism": 70,
                "formatting": 80,
                "ats_friendliness": 78
            }},
            "hrd_consultant_review": "以校招专家身份给出的总体犀利点评与破局建议（150字左右）",
            "hiring_manager_signals": {{
                "strong_signals": [
                    "校招面试官看到的第1个潜力信号",
                    "第2个潜力信号",
                    "第3个潜力信号"
                ],
                "weak_signal": "校招面试官看到的防御红线或最弱能力信号（如缺乏相关项目或实习经验）"
            }},
            "matching_parts_to_highlight": [
                "简历中与校招 JD 高度契合的校园经历/比赛/干部经历1",
                "亮点2"
            ],
            "insufficient_parts_to_supplement": [
                "描述不够充分、需补充具体数据或校园成果的部分1"
            ],
            "enhanced_experience_bullets": [
                {{
                    "original_snippet": "原始校园经历或实习中的平淡描述片段",
                    "optimized_snippet": "润色后话术（运用高级力量感校招动词。修改的关键词用 **[修改后关键词]** 格式高亮标注）",
                    "reason_for_change": "这样修改的校招专家视角解释说服力说明",
                    "quantified_side_note": "【旁侧批注：面试防穿帮】该校园成果在群面或单面被追问时，应如何解释逻辑与推演过程"
                }}
            ],
            "interviewer_hard_questions": [
                {{
                    "question": "校招/实习面试官追问问题1（基于应届生简历）",
                    "intent": "考察意图与解题思路指导"
                }},
                {{
                    "question": "面试官追问问题2",
                    "intent": "考察意图与解题思路指导"
                }},
                {{
                    "question": "面试官追问问题3",
                    "intent": "考察意图与解题思路指导"
                }},
                {{
                    "question": "面试官追问问题4",
                    "intent": "考察意图与解题思路指导"
                }},
                {{
                    "question": "面试官追问问题5",
                    "intent": "考察意图与解题思路指导"
                }}
            ],
            "ats_keywords_must_have": ["校招ATS过筛必备核心关键词1", "关键词2", "关键词3"]
        }}
        """
        return self._call_gemini_json(prompt)