import logging
from fastapi import FastAPI, Depends
from src.adapters.cvat_sdk_adapter import CVATSdkFacade
from src.presentation.web_api.providers.abstract.statistics import statistics_service_provider
from src.interactors.statistics_service import StatisticsService
from src.presentation.web_api.endpoints.statistics import statistics_rout
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler()],)

app = FastAPI()

app.include_router(statistics_rout)


def get_cvat_facade():
    return CVATSdkFacade()


def get_statistics_service(cvat_facade=Depends(get_cvat_facade)):
    return StatisticsService(cvat_facade)


app.dependency_overrides[statistics_service_provider] = get_statistics_service
