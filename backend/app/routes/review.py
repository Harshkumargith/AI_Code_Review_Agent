


# from fastapi import APIRouter
# from app.services.ml_model import predict_code_metrics, predict_text_issue
# from app.services.ai_agent import agent
# from app.models.schema import CodeInput, RepoInput
# from app.utils.repo_utils import clone_repo, read_repo_code

# router = APIRouter()


# # 🔥 Code Review
# @router.post("/review")
# def review(data: CodeInput):

#     # ✅ ML MODELS (BOTH)
#     metric_result = predict_code_metrics(data.code)
#     text_result = predict_text_issue(data.code)

#     # 🤖 AI Agent
#     state = {
#         "code": data.code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(state)

#     return {
#         "analysis": result["initial_analysis"],
#         "issues": result["issues"],
#         "fixed_code": result["fixed_code"],
#         "report": result["final_report"],

#         # ✅ ALL ML OUTPUTS
#         "score": float(metric_result.get("score", 0)),
#         "complexity": metric_result.get("complexity", "unknown"),
#         "label": text_result.get("label", "unknown"),
#     }


# # 🔥 Repo Review
# @router.post("/repo-review")
# def repo_review(data: RepoInput):

#     folder = clone_repo(data.repo_url)
#     code = read_repo_code(folder)

#     metric_result = predict_code_metrics(code)
#     text_result = predict_text_issue(code)

#     state = {
#         "code": code,
#         "initial_analysis": "",
#         "issues": [],
#         "fixed_code": "",
#         "final_report": ""
#     }

#     result = agent.graph.invoke(state)

#     return {
#         "analysis": result["initial_analysis"],
#         "issues": result["issues"],
#         "fixed_code": result["fixed_code"],
#         "report": result["final_report"],

#         "score": float(metric_result.get("score", 0)),
#         "complexity": metric_result.get("complexity", "unknown"),
#         "label": text_result.get("label", "unknown"),
#     }



#-----------------
from fastapi import APIRouter
from app.services.ml_model import predict_code_metrics, predict_text_issue
from app.services.ai_agent import agent
from app.models.schema import CodeInput, RepoInput
from app.utils.repo_utils import clone_repo, read_repo_code


router = APIRouter()


# 🔥 Code Review
@router.post("/review")
def review(data: CodeInput):

    metric_result = predict_code_metrics(data.code)
    text_result = predict_text_issue(data.code)

    state = {
        "code": data.code,
        "initial_analysis": "",
        "issues": [],
        "fixed_code": "",
        "final_report": ""
    }

    result = agent.graph.invoke(state)

    return {
        "analysis": result["initial_analysis"],
        "issues": result["issues"],
        "fixed_code": result["fixed_code"],
        "report": result["final_report"],
        "score": float(metric_result.get("score", 0)),
        "complexity": metric_result.get("complexity", "unknown"),
        "label": text_result.get("label", "unknown"),
    }


# 🔥 Repo Review
@router.post("/repo-review")
def repo_review(data: RepoInput):

    folder = clone_repo(data.repo_url) #Takes the GitHub repo URL from input.
    code = read_repo_code(folder) # Reads all files from the cloned repo. Converts them into a single text/code string.#
    metric_result = predict_code_metrics(code) #Sends code to an ML model.
    text_result = predict_text_issue(code)
#This is the input state for your AI agent.
#It contains:
#raw code
#placeholders for results
    state = {
        "code": code,
        "initial_analysis": "",
        "issues": [],
        "fixed_code": "",
        "final_report": ""
    }
#Calls your AI workflow

    result = agent.graph.invoke(state)

    return {
        "analysis": result["initial_analysis"],
        "issues": result["issues"],
        "fixed_code": result["fixed_code"],
        "report": result["final_report"],
        "score": float(metric_result.get("score", 0)),
        "complexity": metric_result.get("complexity", "unknown"),
        "label": text_result.get("label", "unknown"),
    }


