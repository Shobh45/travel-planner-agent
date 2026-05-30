import os
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fpdf import FPDF

from travelplanneragent.BackEnd.models import TravelRequest, TravelResponse
from travelplanneragent.crew import Travelplanneragent

app = FastAPI(
    title="TravelPlannerAgent API",
    description="FastAPI backend for TravelPlannerAgent Crew integration.",
    version="0.1.0",
)

ROOT_DIR = Path(__file__).resolve().parents[3]
REPORT_FILE = ROOT_DIR / "report.md"


def markdown_to_pdf_bytes(markdown_text: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", size=12)

    for line in markdown_text.splitlines():
        stripped = line.strip()

        if not stripped:
            pdf.ln(4)
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped.lstrip("#").strip()
            font_size = max(16 - (level - 1) * 2, 12)
            pdf.set_font("Helvetica", style="B", size=font_size)
            pdf.multi_cell(0, 8, title)
            pdf.ln(2)
            pdf.set_font("Helvetica", size=12)
            continue

        if stripped.startswith(("- ", "* ")):
            pdf.multi_cell(0, 6, f"• {stripped[2:]}")
            continue

        pdf.multi_cell(0, 6, stripped)

    return pdf.output(dest="S").encode("latin-1", "replace")


@app.get("/", summary="Health check")
def root():
    return {"status": "ok", "message": "TravelPlannerAgent API is running."}


@app.post("/plan", response_model=TravelResponse, summary="Create a travel plan")
def plan_trip(request: TravelRequest):
    inputs = request.dict()

    try:
        crew = Travelplanneragent().crew()
        result = crew.kickoff(inputs=inputs)

        detail = None
        if result is not None:
            detail = str(result)

        if REPORT_FILE.exists():
            report_path = str(REPORT_FILE.relative_to(ROOT_DIR))
        else:
            report_path = None

        return TravelResponse(
            status="success",
            report_file=report_path,
            detail=detail or "Crew kickoff completed successfully.",
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/report", summary="Fetch generated report")
def get_report():
    if not REPORT_FILE.exists():
        raise HTTPException(status_code=404, detail="Report file not found.")

    return JSONResponse(
        content={
            "report_file": str(REPORT_FILE.relative_to(ROOT_DIR)),
            "report": REPORT_FILE.read_text(encoding="utf-8"),
        }
    )


@app.get("/report/pdf", summary="Fetch generated report as PDF")
def get_report_pdf():
    if not REPORT_FILE.exists():
        raise HTTPException(status_code=404, detail="Report file not found.")

    report_text = REPORT_FILE.read_text(encoding="utf-8")

    try:
        pdf_bytes = markdown_to_pdf_bytes(report_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to convert report to PDF: {exc}")

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=travel_report.pdf"},
    )
