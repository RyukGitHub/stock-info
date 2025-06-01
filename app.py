from fastapi import FastAPI, Response
from daily_stock_report import generate_report
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-report")
def generate_report_endpoint():
    filename = generate_report()
    if filename and os.path.exists(filename):
        with open(filename, "rb") as f:
            content = f.read()
        return Response(content, media_type="text/csv", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    return {"error": "Report generation failed"}
