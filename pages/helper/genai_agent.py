import os
import json
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠ GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Safe wrapper to call Gemini
def _call_llm(prompt: str, temperature: float = 0.2, max_tokens: int = 300) -> str:
    """
    Calls Google Gemini API and returns plain text.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )
        return response.text.strip()
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"

# 1) Generate alert text (short, long, markdown). Return dict
def generate_alert(case: Dict[str, Any], tone: str = "neutral") -> Dict[str, str]:
    """
    case: dict containing keys like name, last_seen, location, age, birth_marks, id, submitted_by
    returns: dict with keys 'short', 'long', 'markdown'
    """
    prompt = (
        "You are an assistant that composes concise public missing-person alerts for social media "
        "and formal alerts for police. Keep short version < 200 characters. Provide a longer version "
        "for formal posting and a markdown suitable for social sharing.\n\n"
        f"Case data:\n{json.dumps(case, indent=2)}\n\n"
        "Return JSON with keys: short, long, markdown. Only return valid JSON."
    )

    out = _call_llm(prompt, temperature=0.2, max_tokens=300)

    try:
        return json.loads(out)
    except Exception:
        short = f"Missing: {case.get('name','Unknown')}, last seen at {case.get('last_seen','unknown')}. Call {case.get('phone','-')}."
        long = (
            f"Missing Person Alert\nName: {case.get('name','Unknown')}\n"
            f"Last seen: {case.get('last_seen','Unknown')} at {case.get('address','Unknown')}\n"
            f"Age: {case.get('age','Unknown')}\nDescription: {case.get('description','-')}\n"
            f"Contact: {case.get('submitted_by','-')} / {case.get('phone','-')}\n"
        )
        markdown = f"**Missing: {case.get('name','Unknown')}**  \nLast seen: {case.get('last_seen','Unknown')}  \nContact: {case.get('phone','-')}"
        return {"short": short, "long": long, "markdown": markdown, "raw": out}

# 2) Explain matches
def explain_matches(case: Dict[str, Any], candidates: List[Dict[str, Any]]) -> str:
    prompt = (
        "You are an investigative assistant. Given a registered missing-person case and a list of candidate "
        "public submissions with similarity scores, write a concise explanation why each candidate may match "
        "the missing person (2 sentences max each). Then provide 3 recommended next verification steps.\n\n"
        f"Case: {json.dumps(case, indent=2)}\n\n"
        f"Candidates (showing up to 10): {json.dumps(candidates[:10], indent=2)}\n\nReturn plain text."
    )
    return _call_llm(prompt, temperature=0.2, max_tokens=400)

# 3) Summarize witness text
def summarize_witness(statement: str) -> Dict[str, Any]:
    prompt = (
        "Summarize the following witness statement into 3 concise bullet points, and extract entities: "
        "people, places, times. Return JSON with keys: summary (list), persons (list), places (list), times (list).\n\n"
        f"Statement:\n{statement}\n\nReturn only JSON."
    )
    out = _call_llm(prompt, temperature=0.2, max_tokens=300)
    try:
        return json.loads(out)
    except Exception:
        return {"summary": [statement[:200] + ("..." if len(statement) > 200 else "")], "persons": [], "places": [], "times": [], "raw": out}

# 4) Prioritize leads
def prioritize_leads(leads: List[Dict[str, Any]]) -> str:
    prompt = (
        "Rank these leads by actionability. Each lead has {id, score (higher is better), time_seconds_ago, witness_reliability (0-1)}. "
        "Return a short list of ids in recommended order and three-line justification for the top lead.\n\n"
        f"Leads:\n{json.dumps(leads, indent=2)}"
    )
    return _call_llm(prompt, temperature=0.2, max_tokens=250)
