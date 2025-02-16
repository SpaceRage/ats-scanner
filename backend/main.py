from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_text_from_pdf
from scorer import get_resume_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    return {"text": text}

@app.post("/match/")
async def match_resume(resume_text: str = Form(...), job_description: str = Form(...)):
    score = get_resume_score(resume_text, job_description)
    return {"score": score}
