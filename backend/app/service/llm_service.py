import os
from openai import OpenAI
from ..config import ARK_API_KEY, DOUBAO_MODEL_ID

def optimize_script(text, max_length=50):
    """
    Optimize user input into a speech script using Doubao LLM.
    """
    if not ARK_API_KEY:
        print("Warning: ARK_API_KEY not found. Skipping LLM optimization.")
        return text

    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=ARK_API_KEY,
    )

    system_prompt = (
        "你是一位专业的数字人口语脚本撰写专家。"
        "你的任务是将用户的输入重写为自然、口语化的演讲稿。"
        "规则：\n"
        "1. 仅输出演讲文本。不要包含标题、舞台指导或Markdown格式。\n"
        "2. 文本必须适合直接口语表达。\n"
        f"3. 严格控制长度在 {max_length} 个字符以内。\n"
        "4. 如果输入是问题，请以数字助手的身份简短自然地回答。\n"
        "5. 如果输入是陈述，请优化其流畅度。\n"
        "6. 关键：输出语言必须与输入语言保持一致。"
        "如果输入是中文，必须输出中文。"
        "如果输入是英文，必须输出英文。\n"
        "7. 除非明确要求，否则不要翻译输入内容。"
    )

    try:
        response = client.chat.completions.create(
            model=DOUBAO_MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
        )
        
        content = response.choices[0].message.content.strip()
        print(f"\n[LLM Optimization Log]")
        print(f"Input : {text}")
        print(f"Output: {content}")
        print(f"----------------------\n")
        return content

    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback to original text if LLM fails
        return text
