from typing import Optional

from model import Model
from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion

class GLMModel(Model):
    model: str
    client: ZhipuAI
    
    def __init__(self, model: str, api_key: Optional[str]):
        self.model = model
        self.client = ZhipuAI(api_key=api_key)

    def make_request(self, prompt):
        response: Completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            top_p=0.0,
            stream=False,
            temperature=0.0,
            max_tokens=2000,
        )

        return response.choices[0].message.content, True
