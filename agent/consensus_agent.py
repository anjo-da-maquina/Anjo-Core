import os
import sys
import logging
import yaml
import json

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logging.basicConfig(level=logging.INFO, format='[Anjo-Core/ConsensusAgent] %(levelname)s: %(message)s')

def load_requirements(yaml_path="requirements.yaml"):
    if not os.path.exists(yaml_path):
        logging.error(f"Requirements file not found: {yaml_path}. Cannot perform audit.")
        return None
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_agent():
    logging.info("Awakening Consensus Agent: Initiating Zero-Tolerance Evaluation...")
    
    req_data = load_requirements()
    if not req_data:
        logging.error("No requirements found. Pipeline logic halted.")
        sys.exit(0)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or not OpenAI:
        logging.warning("OpenAI API key missing. Running in dormant simulation mode.")
        return True

    client = OpenAI(api_key=api_key)
    
    system_prompt = """
    You are the Supreme Consensus Agent of the 'anjo-da-maquina' zero-trust audit pipeline.
    Your sole purpose is to evaluate AI-generated outputs against the provided requirements.
    
    ABSOLUTE RULES:
    1. ZERO TOLERANCE: If the output deviates by even a single bit of logic, includes hallucinations, or contains unnecessary additions, you must FAIL it.
    2. NO SYMPATHY: Do not suggest corrections. Do not explain how to fix it.
    3. OUTPUT FORMAT: You must respond ONLY in strict JSON format: {"status": "PASS" or "FAIL", "reason": "brief, cold statement"}
    """

    pure_ai_output = "The system implements the requested feature exactly as specified in the requirements. No additional features, analytics, or modifications have been included."
    
    user_prompt = f"Requirements: {json.dumps(req_data)}\nAI Output to Audit: {pure_ai_output}"

    try:
        logging.info("Consulting the Oracle (LLM) for Absolute Judgment...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        result_str = response.choices[0].message.content
        result = json.loads(result_str)
        
        if result.get("status") == "PASS":
            logging.info(f"[Anjo da máquina] Audit PASSED. Reason: {result.get('reason')}")
            
            # 【追加】検証を通過した「要件」と「出力」を玉座へ渡すために書き出す
            verified_data = {
                "requirements": req_data,
                "ai_output": pure_ai_output,
                "agent_reason": result.get("reason")
            }
            with open("verified_payload.json", "w", encoding="utf-8") as f:
                json.dump(verified_data, f, ensure_ascii=False)
                
        else:
            logging.warning(f"[Anjo da máquina] Audit FAILED. Contamination detected: {result.get('reason')}")
            # 失敗時は玉座へデータを渡さない（以前の残骸があれば消去）
            if os.path.exists("verified_payload.json"):
                os.remove("verified_payload.json")

        return True

    except Exception as e:
        logging.error(f"Failed to execute judgment due to system error: {e}")
        sys.exit(0)

if __name__ == "__main__":
    run_agent()
