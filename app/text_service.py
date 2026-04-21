import os
from openai import OpenAI


class TextService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("缺少 OPENAI_API_KEY 环境变量")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def generate_description(self, detected_labels: list[str], detail: str = "medium") -> str:
        if not detected_labels:
            return "未检测到有效葡萄叶片类别，请重新上传更清晰的图像。"

        category = ", ".join(detected_labels)

        extra = {
            "short": "请用2到3句话简要介绍。",
            "medium": "请用一段完整、自然的中文进行介绍。",
            "long": "请用较详细的一段中文介绍，包括起源、别名、风味特征和主要种植区域。"
        }.get(detail, "请用一段完整、自然的中文进行介绍。")

        prompt = f"""
你是一个葡萄品种科普助手。
请根据识别出的葡萄品种标签，生成适合前端展示的中文说明文字。

识别标签：{category}

要求：
1. 如果只识别到一个品种，就重点介绍该品种。
2. 如果识别到多个标签，优先以第一个标签作为主要品种，同时说明可能检测到相近类别。
3. 内容应包括：起源、别名、风味特征、主要种植区域。
4. 语言自然、准确、适合普通用户阅读。
5. 不要编造无法确认的特别细节。
6. {extra}
"""

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.4,
            max_output_tokens=300,
        )

        return response.output_text.strip()