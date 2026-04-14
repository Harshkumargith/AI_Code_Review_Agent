# from typing import TypedDict, List, Dict
# from langchain_openai import ChatOpenAI
# import os
# from dotenv import load_dotenv
# from langgraph.graph import StateGraph, END
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# # Load env
# load_dotenv()

# # Request model
# class CodeReviewRequest(BaseModel):
#     code: str

# # State
# class CodeReviewState(TypedDict):
#     code: str
#     initial_analysis: str
#     issues: List[str]
#     fixed_code: str
#     final_report: str

# # Agent
# class AdvancedCodeReviewAgent:
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model="gpt-4o-mini",
#             temperature=0.3
#         )

#         self.memory = []
#         self.graph = self._build_graph()

#     # 1️⃣ Analysis
#     def _analysis_agent(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Analyse the code briefly:
# {state['code']}

# Focus on purpose, structure, concerns."""
#         response = self.llm.invoke(prompt)
#         return {"initial_analysis": response.content}

#     # 2️⃣ Issues
#     def _find_issues(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Based on:
# {state['initial_analysis']}

# Code:
# {state['code']}

# List 3-5 issues. Format: - issue"""
#         response = self.llm.invoke(prompt)

#         issues = [
#             line.strip()
#             for line in response.content.split("\n")
#             if line.strip().startswith("-")
#         ]

#         return {"issues": issues}

#     # 3️⃣ Fix
#     def _fix_code(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Fix the code based on issues:

# Code:
# {state['code']}

# Issues:
# {state['issues']}

# Return ONLY improved code."""
#         response = self.llm.invoke(prompt)
#         return {"fixed_code": response.content}

#     # 4️⃣ Report
#     def _generate_report(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Create code review report:

# Analysis:
# {state['initial_analysis']}

# Issues:
# {state['issues']}

# Improved Code:
# {state['fixed_code']}

# Format:
# - Summary
# - Issues
# - Fixed Code
# - Recommendation
# """
#         response = self.llm.invoke(prompt)

#         self.memory.append({
#             "code": state["code"],
#             "issues": state["issues"]
#         })

#         return {"final_report": response.content}

#     # Graph
#     def _build_graph(self) -> StateGraph:
#         workflow = StateGraph(CodeReviewState)

#         workflow.add_node("analyzer", self._analysis_agent)
#         workflow.add_node("issue_finder", self._find_issues)
#         workflow.add_node("fixer", self._fix_code)
#         workflow.add_node("report_generator", self._generate_report)

#         workflow.set_entry_point("analyzer")

#         workflow.add_edge("analyzer", "issue_finder")
#         workflow.add_edge("issue_finder", "fixer")
#         workflow.add_edge("fixer", "report_generator")
#         workflow.add_edge("report_generator", END)

#         return workflow.compile()


# # Init agent
# agent = AdvancedCodeReviewAgent()

# # FastAPI
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # allow frontend
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ======================
# # MAIN API
# # ======================
# @app.post("/review")
# def review_code(request: CodeReviewRequest):
#     initial_state = {
#         "code": request.code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(initial_state)

#     return {
#         "analysis": result["initial_analysis"],
#         "issues": result["issues"],
#         "fixed_code": result["fixed_code"],
#         "report": result["final_report"]
#     }



# from typing import TypedDict, List, Dict
# from langchain_openai import ChatOpenAI
# import os
# import subprocess
# import shutil
# from dotenv import load_dotenv
# from langgraph.graph import StateGraph, END
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# # ======================
# # LOAD ENV
# # ======================
# load_dotenv()

# # ======================
# # REQUEST MODELS
# # ======================
# class CodeReviewRequest(BaseModel):
#     code: str

# class RepoReviewRequest(BaseModel):
#     repo_url: str

# # ======================
# # STATE TYPE
# # ======================
# class CodeReviewState(TypedDict):
#     code: str
#     initial_analysis: str
#     issues: List[str]
#     fixed_code: str
#     final_report: str

# # ======================
# # AGENT
# # ======================
# class AdvancedCodeReviewAgent:
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model="gpt-4o-mini",
#             temperature=0.3
#         )

#         self.memory = []
#         self.graph = self._build_graph()

#     # 1️⃣ Analysis
#     def _analysis_agent(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Analyse the code briefly:
# {state['code']}

# Focus on:
# - Purpose
# - Structure
# - Key concerns"""
#         response = self.llm.invoke(prompt)
#         return {"initial_analysis": response.content}

#     # 2️⃣ Issues
#     def _find_issues(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Based on analysis:
# {state['initial_analysis']}

# Code:
# {state['code']}

# List 3-5 issues. Format strictly:
# - issue"""
#         response = self.llm.invoke(prompt)

#         issues = [
#             line.strip()
#             for line in response.content.split("\n")
#             if line.strip().startswith("-")
#         ]

#         return {"issues": issues}

#     # 3️⃣ Fix
#     def _fix_code(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Fix the code based on issues:

# Code:
# {state['code']}

# Issues:
# {state['issues']}

# Return ONLY improved code."""
#         response = self.llm.invoke(prompt)
#         return {"fixed_code": response.content}

#     # 4️⃣ Report
#     def _generate_report(self, state: CodeReviewState) -> Dict:
#         prompt = f"""Create a structured code review report:

# Analysis:
# {state['initial_analysis']}

# Issues:
# {state['issues']}

# Improved Code:
# {state['fixed_code']}

# Format:
# - Summary
# - Issues
# - Fix Explanation
# - Recommendation
# """
#         response = self.llm.invoke(prompt)

#         self.memory.append({
#             "code": state["code"],
#             "issues": state["issues"]
#         })

#         return {"final_report": response.content}

#     # GRAPH
#     def _build_graph(self) -> StateGraph:
#         workflow = StateGraph(CodeReviewState)

#         workflow.add_node("analyzer", self._analysis_agent)
#         workflow.add_node("issue_finder", self._find_issues)
#         workflow.add_node("fixer", self._fix_code)
#         workflow.add_node("report_generator", self._generate_report)

#         workflow.set_entry_point("analyzer")

#         workflow.add_edge("analyzer", "issue_finder")
#         workflow.add_edge("issue_finder", "fixer")
#         workflow.add_edge("fixer", "report_generator")
#         workflow.add_edge("report_generator", END)

#         return workflow.compile()


# # ======================
# # INIT
# # ======================
# agent = AdvancedCodeReviewAgent()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ======================
# # NORMAL CODE REVIEW
# # ======================
# @app.post("/review")
# def review_code(request: CodeReviewRequest):
#     initial_state = {
#         "code": request.code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(initial_state)

#     return {
#         "analysis": result["initial_analysis"],
#         "issues": result["issues"],
#         "fixed_code": result["fixed_code"],
#         "report": result["final_report"],
#         "score": "8/10"
#     }

# # ======================
# # GITHUB REPO REVIEW (FIXED)
# # ======================
# @app.post("/repo-review")
# def repo_review(request: RepoReviewRequest):
#     try:
#         repo_url = request.repo_url.strip().replace(".git", "")
#         repo_path = "temp_repo"

#         # 🔥 Remove old repo
#         if os.path.exists(repo_path):
#             shutil.rmtree(repo_path)

#         # 🔥 Clone repo
#         subprocess.run(
#             ["git", "clone", repo_url, repo_path],
#             check=True,
#             timeout=30
#         )

#         code_data = ""

#         # 🔥 Read files safely
#         for root, _, files in os.walk(repo_path):
#             for file in files:
#                 if file.endswith((".py", ".cpp", ".js", ".ts", ".java")):
#                     file_path = os.path.join(root, file)

#                     try:
#                         with open(file_path, "r", errors="ignore") as f:
#                             content = f.read()
#                             code_data += content[:2000] + "\n\n"
#                     except:
#                         continue

#         if not code_data:
#             return {
#                 "analysis": "No readable code found in repository",
#                 "issues": [],
#                 "fixed_code": "",
#                 "report": "",
#                 "score": "0/10"
#             }

#         # 🔥 Limit size (important)
#         code_data = code_data[:8000]

#         # 🔥 Run agent
#         initial_state = {
#             "code": code_data,
#             "initial_analysis": "",
#             "issues": [],
#             "fixed_code": "",
#             "final_report": ""
#         }

#         result = agent.graph.invoke(initial_state)

#         return {
#             "analysis": result["initial_analysis"],
#             "issues": result["issues"],
#             "fixed_code": result["fixed_code"],
#             "report": result["final_report"],
#             "score": "8/10"
#         }

#     except Exception as e:
#         return {
#             "analysis": f"Error analyzing repository: {str(e)}",
#             "issues": [],
#             "fixed_code": "",
#             "report": "",
#             "score": "0/10"
#         }

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import TypedDict, List, Dict
# from dotenv import load_dotenv

# import os
# import subprocess
# import shutil

# from langchain_openai import ChatOpenAI
# from langgraph.graph import StateGraph, END

# from app.services.ml_model import predict_code_metrics

# # ======================
# # LOAD ENV
# # ======================
# load_dotenv()

# # ======================
# # FASTAPI INIT
# # ======================
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ======================
# # REQUEST MODELS
# # ======================
# class CodeReviewRequest(BaseModel):
#     code: str

# class RepoReviewRequest(BaseModel):
#     repo_url: str

# # ======================
# # STATE TYPE
# # ======================
# class CodeReviewState(TypedDict):
#     code: str
#     initial_analysis: str
#     issues: List[str]
#     fixed_code: str
#     final_report: str

# # ======================
# # AGENT
# # ======================
# class AdvancedCodeReviewAgent:
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model="gpt-4o-mini",
#             temperature=0.3,
#             api_key=os.getenv("OPENAI_API_KEY")  # ✅ FIXED
#         )

#         self.graph = self._build_graph()

#     # 🔥 SAFE CALL (NO CRASH)
#     def safe_llm(self, prompt):
#         try:
#             return self.llm.invoke(prompt).content
#         except Exception as e:
#             print("LLM ERROR:", e)
#             return "⚠ AI temporarily unavailable"

#     def _analysis_agent(self, state: CodeReviewState) -> Dict:
#         prompt = f"Analyse code:\n{state['code']}"
#         return {"initial_analysis": self.safe_llm(prompt)}

#     def _find_issues(self, state: CodeReviewState) -> Dict:
#         prompt = f"Find issues:\n{state['code']}"
#         response = self.safe_llm(prompt)

#         issues = [
#             line.strip()
#             for line in response.split("\n")
#             if line.strip().startswith("-")
#         ]

#         return {"issues": issues if issues else ["No major issues detected"]}

#     def _fix_code(self, state: CodeReviewState) -> Dict:
#         prompt = f"Fix code:\n{state['code']}"
#         return {"fixed_code": self.safe_llm(prompt)}

#     def _generate_report(self, state: CodeReviewState) -> Dict:
#         prompt = f"""
# Generate report:
# {state['initial_analysis']}
# {state['issues']}
# {state['fixed_code']}
# """
#         return {"final_report": self.safe_llm(prompt)}

#     def _build_graph(self) -> StateGraph:
#         workflow = StateGraph(CodeReviewState)

#         workflow.add_node("analyzer", self._analysis_agent)
#         workflow.add_node("issues", self._find_issues)
#         workflow.add_node("fix", self._fix_code)
#         workflow.add_node("report", self._generate_report)

#         workflow.set_entry_point("analyzer")

#         workflow.add_edge("analyzer", "issues")
#         workflow.add_edge("issues", "fix")
#         workflow.add_edge("fix", "report")
#         workflow.add_edge("report", END)

#         return workflow.compile()


# # ======================
# # INIT AGENT
# # ======================
# agent = AdvancedCodeReviewAgent()

# # ======================
# # CODE REVIEW API
# # ======================
# @app.post("/review")
# def review_code(request: CodeReviewRequest):

#     state = {
#         "code": request.code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(state)

#     # 🔥 ML
#     try:
#         ml_result = predict_code_metrics(request.code)
#     except:
#         ml_result = {"score": 0, "complexity": "unknown"}

#     return {
#         "analysis": result.get("initial_analysis", ""),
#         "issues": result.get("issues", []),
#         "fixed_code": result.get("fixed_code", ""),
#         "report": result.get("final_report", ""),
#         "score": ml_result["score"],
#         "complexity": ml_result["complexity"]
#     }


# # ======================
# # REPO REVIEW API
# # ======================
# @app.post("/repo-review")
# def repo_review(request: RepoReviewRequest):

#     try:
#         repo_url = request.repo_url.strip().replace(".git", "")
#         repo_path = "temp_repo"

#         if os.path.exists(repo_path):
#             shutil.rmtree(repo_path)

#         subprocess.run(
#             ["git", "clone", repo_url, repo_path],
#             check=True,
#             timeout=30
#         )

#         code_data = ""

#         for root, _, files in os.walk(repo_path):
#             for file in files:
#                 if file.endswith((".py", ".cpp", ".js", ".java")):
#                     try:
#                         with open(os.path.join(root, file), "r", errors="ignore") as f:
#                             code_data += f.read()[:2000] + "\n\n"
#                     except:
#                         continue

#         code_data = code_data[:8000]

#         state = {
#             "code": code_data,
#             "initial_analysis": "",
#             "issues": [],
#             "fixed_code": "",
#             "final_report": ""
#         }

#         result = agent.graph.invoke(state)

#         try:
#             ml_result = predict_code_metrics(code_data)
#         except:
#             ml_result = {"score": 0, "complexity": "unknown"}

#         return {
#             "analysis": result.get("initial_analysis", ""),
#             "issues": result.get("issues", []),
#             "fixed_code": result.get("fixed_code", ""),
#             "report": result.get("final_report", ""),
#             "score": ml_result["score"],
#             "complexity": ml_result["complexity"]
#         }

#     except Exception as e:
#         return {
#             "analysis": f"Error: {str(e)}",
#             "issues": [],
#             "fixed_code": "",
#             "report": "",
#             "score": 0,
#             "complexity": "unknown"  # ✅ FIXED
#         }
        

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse


import os
import subprocess
import shutil

# 🔥 AI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# 🔥 ML (BOTH MODELS)
from app.services.ml_model import predict_code_metrics, predict_text_issue

# ======================
# LOAD ENV
# ======================
load_dotenv()

# ======================
# FASTAPI INIT
# ======================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# REQUEST MODELS
# ======================
class CodeReviewRequest(BaseModel):
    code: str

class RepoReviewRequest(BaseModel):
    repo_url: str

# ======================
# STATE TYPE
# ======================
class CodeReviewState(TypedDict):
    code: str
    initial_analysis: str
    issues: List[str]
    fixed_code: str
    final_report: str

# ======================
# AI AGENT
# ======================
class AdvancedCodeReviewAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.graph = self._build_graph()

    # 🔥 SAFE CALL
    def safe_llm(self, prompt):
        try:
            return self.llm.invoke(prompt).content
        except Exception as e:
            print("LLM ERROR:", e)
            return "⚠ AI temporarily unavailable"

    def _analysis_agent(self, state: CodeReviewState) -> Dict:
        prompt = f"Analyse code:\n{state['code']}"
        return {"initial_analysis": self.safe_llm(prompt)}

    def _find_issues(self, state: CodeReviewState) -> Dict:
        prompt = f"Find issues:\n{state['code']}"
        response = self.safe_llm(prompt)

        issues = [
            line.strip()
            for line in response.split("\n")
            if line.strip().startswith("-")
        ]

        return {"issues": issues if issues else ["No major issues detected"]}

    def _fix_code(self, state: CodeReviewState) -> Dict:
        prompt = f"Fix code:\n{state['code']}"
        return {"fixed_code": self.safe_llm(prompt)}

    def _generate_report(self, state: CodeReviewState) -> Dict:
        prompt = f"""
Generate report:
{state['initial_analysis']}
{state['issues']}
{state['fixed_code']}
"""
        return {"final_report": self.safe_llm(prompt)}

    def _build_graph(self) -> StateGraph:
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


# ======================
# INIT AGENT
# ======================
agent = AdvancedCodeReviewAgent()

# ======================
# CODE REVIEW API
# ======================
@app.post("/review")
def review_code(request: CodeReviewRequest):

    state = {
        "code": request.code,
        "initial_analysis": "",
        "issues": [],
        "fixed_code": "",
        "final_report": ""
    }

    result = agent.graph.invoke(state)

    # 🔥 ML (BOTH)
    try:
        metric_result = predict_code_metrics(request.code)
        text_result = predict_text_issue(request.code)

        print("METRIC:", metric_result)
        print("LABEL:", text_result)

    except Exception as e:
        print("ML ERROR:", e)
        metric_result = {"score": 0, "complexity": "unknown"}
        text_result = {"label": "unknown"}

    return {
        "analysis": result.get("initial_analysis", ""),
        "issues": result.get("issues", []),
        "fixed_code": result.get("fixed_code", ""),
        "report": result.get("final_report", ""),

        # ✅ FINAL OUTPUT
        "score": float(metric_result.get("score", 0)),
        "complexity": metric_result.get("complexity", "unknown"),
        "label": text_result.get("label", "unknown"),
    }


# ======================
# REPO REVIEW API
# ======================
@app.post("/repo-review")
def repo_review(request: RepoReviewRequest):

    try:
        repo_url = request.repo_url.strip().replace(".git", "")
        repo_path = "temp_repo"

        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True,
            timeout=30
        )

        code_data = ""

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".py", ".cpp", ".js", ".java")):
                    try:
                        with open(os.path.join(root, file), "r", errors="ignore") as f:
                            code_data += f.read()[:2000] + "\n\n"
                    except:
                        continue

        code_data = code_data[:8000]

        state = {
            "code": code_data,
            "initial_analysis": "",
            "issues": [],
            "fixed_code": "",
            "final_report": ""
        }

        result = agent.graph.invoke(state)

        # 🔥 ML
        try:
            metric_result = predict_code_metrics(code_data)
            text_result = predict_text_issue(code_data)
        except:
            metric_result = {"score": 0, "complexity": "unknown"}
            text_result = {"label": "unknown"}

        return {
            "analysis": result.get("initial_analysis", ""),
            "issues": result.get("issues", []),
            "fixed_code": result.get("fixed_code", ""),
            "report": result.get("final_report", ""),

            # ✅ FINAL OUTPUT
            "score": float(metric_result.get("score", 0)),
            "complexity": metric_result.get("complexity", "unknown"),
            "label": text_result.get("label", "unknown"),
        }

    except Exception as e:
        return {
            "analysis": f"Error: {str(e)}",
            "issues": [],
            "fixed_code": "",
            "report": "",
            "score": 0,
            "complexity": "unknown",
            "label": "unknown"
        }

  
