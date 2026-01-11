from app.core.ai_brain import SentinelBrain

# Initialize the brain with the 'Smart' model (Claude 3.5 Sonnet)
agent = SentinelBrain(provider="anthropic")

def analyze_code_logic(requirements: str, code_diff: str):
    """
    Compares the business requirements against the actual code changes.
    """
    
    system_prompt = """
    ROLE: You are the 'Semantic Guardrail' - a Senior Logic Auditor.
    
    GOAL: Identify if the provided code changes (Diff) contradict or fail to 
    implement the business requirements (Intent).
    
    CRITERIA:
    1. If a requirement is missing in the code -> FAIL.
    2. If the code logic contradicts a requirement -> FAIL.
    3. If the code is correct and follows intent -> PASS.
    
    OUTPUT FORMAT:
    Your response must start with either 'PASS' or 'FAIL'. 
    If FAIL, provide a bulleted list of the specific logic violations.
    """

    user_message = f"""
    BUSINESS REQUIREMENTS:
    {requirements}

    CODE DIFF TO AUDIT:
    {code_diff}
    """

    # Get the verdict from the AI
    verdict = agent.ask(system_prompt, user_message)
    return verdict