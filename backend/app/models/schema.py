from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str

class RepoInput(BaseModel):
    repo_url: str