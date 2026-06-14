from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google MCP Server")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Google MCP Server is running. Visit /docs for API documentation."}

class DocRequest(BaseModel):
    doc_id: str
    content: str

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

import os

def ask_approval(action_name: str, payload: dict) -> bool:
    print(f"\n--- Action Requested ---")
    print(f"Action: {action_name}")
    print(f"Payload: {payload}")
    
    if os.getenv("BYPASS_APPROVAL", "").lower() == "true":
        print("Bypassing manual approval due to BYPASS_APPROVAL=true environment variable.")
        return True
    
    while True:
        response = input("Approve? (y/n): ").strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please answer 'y' or 'n'.")

@app.post("/append_to_doc")
def append_doc_endpoint(req: DocRequest):
    approved = ask_approval("append_to_doc", req.model_dump())
    if not approved:
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    try:
        result = append_to_doc(req.doc_id, req.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_email_draft")
def create_draft_endpoint(req: EmailRequest):
    approved = ask_approval("create_email_draft", req.model_dump())
    if not approved:
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    try:
        result = create_email_draft(req.to, req.subject, req.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
