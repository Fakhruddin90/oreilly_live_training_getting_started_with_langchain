# /// script
# requires-python = ">=3.12"
# dependencies = ["langchain>=1.0", "langchain-openai"]
# ///

from pydantic import BaseModel, Field
from langchain.agents import create_agent

# Define the structure of your report
class DailyReport(BaseModel):
    """A structured daily report with summary, metrics, and action items."""
    summary: str = Field(description="A brief summary of the day's activities.")
    key_metrics: dict = Field(description="Dictionary of key performance metrics.")
    action_items: list[str] = Field(description="List of follow-up tasks.")

# Configure the agent with your schema
agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    system_prompt=(
        "You are a business analyst that generates structured daily reports. "
        "When asked about a team's day, produce a detailed report with a summary, "
        "key metrics (as a dictionary), and actionable follow-up items."
    ),
    response_format=DailyReport,
)

# Invoke the agent
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Generate a daily report for the engineering team. "
                "Today we shipped the new auth feature, fixed 3 critical bugs, "
                "and onboarded 2 new developers."
            ),
        }
    ]
})

# Access the structured data directly
if result.get("structured_response"):
    report: DailyReport = result["structured_response"]
    print("=== Daily Report ===")
    print(f"\nSummary: {report.summary}")
    print(f"\nKey Metrics: {report.key_metrics}")
    print("\nAction Items:")
    for i, item in enumerate(report.action_items, 1):
        print(f"  {i}. {item}")
else:
    print("No structured response — fallback:")
    print(result["messages"][-1].content)