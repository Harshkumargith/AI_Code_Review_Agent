# from fastapi import FastAPI  # FastAPI framework import for building APIs
# from fastapi.middleware.cors import CORSMiddleware  # Enables cross-origin requests
# from pydantic import BaseModel  # Used for request validation
# from typing import TypedDict, List, Dict  # Type hints for better structure
# from dotenv import load_dotenv  # Load environment variables from .env file
# from fastapi.responses import StreamingResponse  # Used for streaming responses

# import os  # OS operations like file handling
# import subprocess  # Run system commands like git clone
# import shutil  # File/folder operations (delete etc.)

# # 🔥 AI
# from langchain_openai import ChatOpenAI  # LLM model integration
# from langgraph.graph import StateGraph, END  # Workflow graph system

# # 🔥 ML (BOTH MODELS)
# from app.services.ml_model import predict_code_metrics, predict_text_issue  # ML models

# # ======================
# # LOAD ENV
# # ======================
# load_dotenv()  # Load API keys and configs from .env file

# # ======================
# # FASTAPI INIT
# # ======================
# app = FastAPI()  # Create FastAPI app instance

# app.add_middleware(
#     CORSMiddleware,  # Add CORS middleware
#     allow_origins=["*"],  # Allow all origins (frontend access)
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # ======================
# # REQUEST MODELS
# # ======================
# class CodeReviewRequest(BaseModel):  # Request model for code input
#     code: str  # Accept code as string

# class RepoReviewRequest(BaseModel):  # Request model for repo input
#     repo_url: str  # Accept GitHub repo URL

# # ======================
# # STATE TYPE
# # ======================
# class CodeReviewState(TypedDict):  # Structure for agent workflow state
#     code: str  # Input code
#     initial_analysis: str  # AI analysis
#     issues: List[str]  # List of issues
#     fixed_code: str  # Improved code
#     final_report: str  # Final report

# # ======================
# # AI AGENT
# # ======================
# class AdvancedCodeReviewAgent:  # Main AI agent class
#     def __init__(self):
#         self.llm = ChatOpenAI(  # Initialize OpenAI model
#             model="gpt-4o-mini",  # Model name
#             temperature=0.3,  # Low randomness for accuracy
#             api_key=os.getenv("OPENAI_API_KEY")  # API key from env
#         )

#         self.graph = self._build_graph()  # Build workflow graph

#     # 🔥 SAFE CALL
#     def safe_llm(self, prompt):
#         try:
#             return self.llm.invoke(prompt).content  # Call LLM safely
#         except Exception as e:
#             print("LLM ERROR:", e)  # Print error
#             return "⚠ AI temporarily unavailable"  # Fallback message

#     def _analysis_agent(self, state: CodeReviewState) -> Dict:
#         prompt = f"Analyse code:\n{state['code']}"  # Create prompt
#         return {"initial_analysis": self.safe_llm(prompt)}  # Return analysis

#     def _find_issues(self, state: CodeReviewState) -> Dict:
#         prompt = f"Find issues:\n{state['code']}"  # Prompt for issues
#         response = self.safe_llm(prompt)  # Get response

#         issues = [
#             line.strip()  # Clean line
#             for line in response.split("\n")  # Split response
#             if line.strip().startswith("-")  # Extract bullet points
#         ]

#         return {"issues": issues if issues else ["No major issues detected"]}  # Return issues

#     def _fix_code(self, state: CodeReviewState) -> Dict:
#         prompt = f"Fix code:\n{state['code']}"  # Prompt for fixing code
#         return {"fixed_code": self.safe_llm(prompt)}  # Return fixed code

#     def _generate_report(self, state: CodeReviewState) -> Dict:
#         prompt = f"""
# Generate report:
# {state['initial_analysis']}
# {state['issues']}
# {state['fixed_code']}
# """  # Combine all outputs
#         return {"final_report": self.safe_llm(prompt)}  # Generate final report

#     def _build_graph(self) -> StateGraph:
#         workflow = StateGraph(CodeReviewState)  # Create workflow graph

#         workflow.add_node("analyzer", self._analysis_agent)  # Add analysis step
#         workflow.add_node("issues", self._find_issues)  # Add issue detection
#         workflow.add_node("fix", self._fix_code)  # Add fix step
#         workflow.add_node("report", self._generate_report)  # Add report step

#         workflow.set_entry_point("analyzer")  # Start from analyzer

#         workflow.add_edge("analyzer", "issues")  # Flow: analyzer → issues
#         workflow.add_edge("issues", "fix")  # Flow: issues → fix
#         workflow.add_edge("fix", "report")  # Flow: fix → report
#         workflow.add_edge("report", END)  # End workflow

#         return workflow.compile()  # Compile graph

# # ======================
# # INIT AGENT
# # ======================
# agent = AdvancedCodeReviewAgent()  # Create agent instance

# # ======================
# # CODE REVIEW API
# # ======================
# @app.post("/review")  # API endpoint for code review
# def review_code(request: CodeReviewRequest):

#     state = {  # Initial state
#         "code": request.code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(state)  # Run AI workflow

#     # 🔥 ML (BOTH)
#     try:
#         metric_result = predict_code_metrics(request.code)  # Predict metrics
#         text_result = predict_text_issue(request.code)  # Predict label

#         print("METRIC:", metric_result)  # Debug print
#         print("LABEL:", text_result)

#     except Exception as e:
#         print("ML ERROR:", e)  # Error handling
#         metric_result = {"score": 0, "complexity": "unknown"}  # Default values
#         text_result = {"label": "unknown"}

#     return {
#         "analysis": result.get("initial_analysis", ""),  # Return analysis
#         "issues": result.get("issues", []),  # Return issues
#         "fixed_code": result.get("fixed_code", ""),  # Return fixed code
#         "report": result.get("final_report", ""),  # Return report

#         "score": float(metric_result.get("score", 0)),  # Return score
#         "complexity": metric_result.get("complexity", "unknown"),  # Complexity
#         "label": text_result.get("label", "unknown"),  # Label
#     }

# # ======================
# # REPO REVIEW API
# # ======================
# @app.post("/repo-review")  # API endpoint for repo review
# def repo_review(request: RepoReviewRequest):

#     try:
#         repo_url = request.repo_url.strip().replace(".git", "")  # Clean URL
#         repo_path = "temp_repo"  # Temp folder name

#         if os.path.exists(repo_path):
#             shutil.rmtree(repo_path)  # Delete old repo

#         subprocess.run(
#             ["git", "clone", repo_url, repo_path],  # Clone repo
#             check=True,
#             timeout=30  # Timeout for safety
#         )

#         code_data = ""  # Store all code

#         for root, _, files in os.walk(repo_path):  # Traverse files
#             for file in files:
#                 if file.endswith((".py", ".cpp", ".js", ".java")):  # Filter code files
#                     try:
#                         with open(os.path.join(root, file), "r", errors="ignore") as f:
#                             code_data += f.read()[:2000] + "\n\n"  # Read limited content
#                     except:
#                         continue  # Skip error files

#         code_data = code_data[:8000]  # Limit total size

#         state = {  # Create state
#             "code": code_data,
#             "initial_analysis": "",
#             "issues": [],
#             "fixed_code": "",
#             "final_report": ""
#         }

#         result = agent.graph.invoke(state)  # Run AI agent

#         # 🔥 ML
#         try:
#             metric_result = predict_code_metrics(code_data)  # Metrics
#             text_result = predict_text_issue(code_data)  # Label
#         except:
#             metric_result = {"score": 0, "complexity": "unknown"}  # Default
#             text_result = {"label": "unknown"}

#         return {
#             "analysis": result.get("initial_analysis", ""),  # Analysis
#             "issues": result.get("issues", []),  # Issues
#             "fixed_code": result.get("fixed_code", ""),  # Fixed code
#             "report": result.get("final_report", ""),  # Report

#             "score": float(metric_result.get("score", 0)),  # Score
#             "complexity": metric_result.get("complexity", "unknown"),  # Complexity
#             "label": text_result.get("label", "unknown"),  # Label
#         }

#     except Exception as e:
#         return {
#             "analysis": f"Error: {str(e)}",  # Error message
#             "issues": [],
#             "fixed_code": "",
#             "report": "",
#             "score": 0,
#             "complexity": "unknown",
#             "label": "unknown"
#         }













from fastapi import FastAPI # FastAPI framework import for building APIs
from fastapi.middleware.cors import CORSMiddleware ## Enables cross-origin requests
from pydantic import BaseModel  # Used for request validation
from pydantic import BaseModel #
from typing import TypedDict, List, Dict # # Type hints for better structure
from dotenv import load_dotenv ## Load environment variables from .env file
from fastapi.responses import StreamingResponse ## Used for streaming responses


import os # OS operations like file handling
import subprocess  # Run system commands like git clone
import shutil   # File/folder operations (delete etc.)


# 🔥 AI
from langchain_openai import ChatOpenAI # LLM model integration
from langgraph.graph import StateGraph, END  # Workflow graph system

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



