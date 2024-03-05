
from datetime import datetime
import os
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, BackgroundTasks
from src.interactors.statistics_service import StatisticsService
from src.presentation.web_api.providers.abstract.statistics import statistics_service_provider
from src.presentation.web_api.dependencies.depends_stub import Stub
from src.presentation.web_api.schemas.statistic import Assignee
import openpyxl

statistics_rout = APIRouter(tags=['statistic'])

def generate_filename(assignee_username: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{assignee_username}_{timestamp}.xlsx"

@statistics_rout.post("/statistics/json")
def get_statistics_by_assignee_as_json(assignee: Assignee, statistics_service: StatisticsService = Depends(Stub(statistics_service_provider))):
    return statistics_service.get_statistics_by_assignee(assignee.username)


@statistics_rout.post("/statistics/xlsx", response_class=FileResponse)
def get_statistics_by_assignee_as_xlsx(assignee: Assignee,
                                        background_tasks: BackgroundTasks,
                                        statistics_service: StatisticsService = Depends(Stub(statistics_service_provider))):
    stats_data = statistics_service.get_statistics_by_assignee(assignee.username)
    filename = generate_filename(assignee.username)
    wb = openpyxl.Workbook()
    ws = wb.active
    headers = ["job_id", "stage", "bbox_count"]
    ws.append(headers)
    bbox_total = 0
    for job in stats_data.get("jobs", []):
        row = [job.get(header) for header in headers]
        ws.append(row)
        bbox_total += job.get("bbox_count", 0)

    ws.append(["bbox_total", "", bbox_total])

    file_path = filename

    wb.save(file_path)
    background_tasks.add_task(cleanup_file, file_path)

    return FileResponse(path=file_path,
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        headers={"Content-Disposition": f"attachment; filename={filename}"})


def cleanup_file(file_path):
        os.remove(file_path)
    