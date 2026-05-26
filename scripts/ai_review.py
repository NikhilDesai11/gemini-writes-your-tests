from google import genai
import sys
import json

client = genai.Client()


def review_code(diff_text):
    """Send a code diff to Gemini and get structured JSON review."""

    prompt = f"""
You are an expert code reviewer.

Return ONLY valid JSON. No explanations, no markdown, no extra text.

JSON format:
{{
  "issues": [
    {{
      "severity": "HIGH | MEDIUM | LOW",
      "description": "string",
      "suggested_fix": "string"
    }}
  ],
  "summary": "CRITICAL | WARNING | GOOD"
}}

Rules:
- summary = "CRITICAL" if ANY HIGH severity issues exist
- summary = "WARNING" if only MEDIUM/LOW issues exist
- summary = "GOOD" if no issues exist
- If no issues are found, return: "issues": []

Focus on:
1. Security vulnerabilities
2. Bug risks
3. Performance issues
4. Best practice violations

Code diff:
{diff_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def parse_severity(review_text):
    """Extract severity level from the review output."""
    for line in review_text.strip().split("\n"):
        if line.strip().startswith("SEVERITY_SUMMARY:"):
            level = line.split(":", 1)[1].strip().upper()
            if level in ("CRITICAL", "WARNING", "GOOD"):
                return level
    return "WARNING"  # Default to WARNING if parsing fails


if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        with open(diff_file, "r", encoding="utf-8") as f:
            diff_content = f.read()
    else:
        diff_content = sys.stdin.read()

    review = review_code(diff_content)

    severity = parse_severity(review)

    try:
        result = json.loads(review)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print("Failed to parse model output as JSON:")
        print(review)

    with open("severity.txt", "w") as f:
        f.write(severity)