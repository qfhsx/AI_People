from app.service.llm_service import optimize_script

if __name__ == "__main__":
    print("Testing LLM optimization logging...")
    result = optimize_script("你好，你是谁？")
    print(f"Final Result: {result}")
