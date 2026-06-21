"""
Morning Article Pipeline Digest
Alpha Strategies — Jay Rogers
Runs daily via GitHub Actions at 6:00 AM PT
"""

import anthropic
import datetime
import os
import pathlib

PROMPT = """You are a research assistant for a conservative financial and policy writer
with an active op-ed pipeline. Search the web for news published in the last 24 hours
across these topic clusters and return a digest under 800 words.

CLUSTER 1 — Constitutional & Law Enforcement
Keywords: Fourth Amendment, Tenth Amendment, Commerce Clause, SCOTUS rulings,
federal preemption, civil asset forfeiture, eminent domain

CLUSTER 2 — Military & National Security
Keywords: defense budget, Pentagon spending, military readiness, veterans policy,
Special Forces, Army aviation, national security legislation

CLUSTER 3 — National Debt & Fiscal Policy
Keywords: federal deficit, national debt ceiling, CBO projections, entitlement reform,
Social Security, Medicare solvency, federal spending

CLUSTER 4 — Public Pension & Fiduciary Duty
Keywords: public pension funding, CalPERS, LEOFF, fiduciary duty, pension reform,
ESG investing mandates, state pension liability

CLUSTER 5 — ESG & Regulatory
Keywords: ESG regulation, SEC rulemaking, proxy voting, DEI mandates,
investment fiduciary standards, private equity regulation

FORMAT:
- Group findings by cluster
- Lead each item with the publication name and date
- One sentence summary per item
- Flag any item directly relevant to an active op-ed topic with [PIPELINE HIT]
- End with a 2-sentence editorial note on the strongest story of the day

Keep the tone dry and professional. No filler. No bullet padding."""


def run_digest() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": PROMPT}],
    )

    # Extract all text blocks from the response
    output = []
    for block in response.content:
        if hasattr(block, "text"):
            output.append(block.text)

    return "\n\n".join(output) if output else "No digest content returned."


def save_digest(content: str) -> pathlib.Path:
    today = datetime.date.today().isoformat()
    output_dir = pathlib.Path("digests")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{today}.md"

    timestamp = datetime.datetime.now().strftime("%B %d, %Y — %I:%M %p PT")
    full_content = f"# Morning Article Pipeline Digest\n**{timestamp}**\n\n{content}"

    output_path.write_text(full_content, encoding="utf-8")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Running Morning Article Pipeline Digest...")
    digest = run_digest()
    print(digest)
    save_digest(digest)
