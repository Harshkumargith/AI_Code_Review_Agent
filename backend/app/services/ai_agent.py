from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict

class CodeReviewState(TypedDict):
    code: str
    initial_analysis: str
    issues: List[str]
    fixed_code: str
    final_report: str


class AdvancedCodeReviewAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )
        self.graph = self._build_graph()

    def _analysis_agent(self, state: CodeReviewState) -> Dict:
        prompt = f"Analyze this code:\n{state['code']}"
        res = self.llm.invoke(prompt)
        return {"initial_analysis": res.content}

    def _find_issues(self, state: CodeReviewState) -> Dict:
        prompt = f"Find issues:\n{state['code']}"
        res = self.llm.invoke(prompt)

        issues = [line for line in res.content.split("\n") if line.startswith("-")]
        return {"issues": issues}

    def _fix_code(self, state: CodeReviewState) -> Dict:
        prompt = f"Fix code:\n{state['code']}"
        res = self.llm.invoke(prompt)
        return {"fixed_code": res.content}

    def _generate_report(self, state: CodeReviewState) -> Dict:
        prompt = f"Generate report:\n{state['code']}"
        res = self.llm.invoke(prompt)
        return {"final_report": res.content}

    def _build_graph(self):
        workflow = StateGraph(CodeReviewState)

        workflow.add_node("analyzer", self._analysis_agent)
        workflow.add_node("issues", self._find_issues)
        workflow.add_node("fix", self._fix_code)
        workflow.add_node("report", self._generate_report)

        workflow.set_entry_point("analyzer")
        workflow.add_edge("analyzer", "issues")
        workflow.add_edge("issues", "fix")
        workflow.add_edge("fix", "report")
        workflow.add_edge("report", END)

        return workflow.compile()


# 🔥 initialize
agent = AdvancedCodeReviewAgent()