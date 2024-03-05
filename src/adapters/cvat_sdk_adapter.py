from abc import ABC, abstractmethod
from cvat_sdk.api_client import Configuration, ApiClient


class CVATSdkFacadeInterface(ABC):
    @abstractmethod
    def get_statistics_by_assignee(self, assignee: str):
        pass


class CVATSdkFacade(CVATSdkFacadeInterface):

    
    configuration = Configuration(host="https://app.cvat.ai/", username='huseinnaimov@bk.ru',
                                  password='Husia2000',)

    def get_statistics_by_assignee(self, assignee: str):
        bbox_total = 0
        assignee_jobs_statistics = []
        job_id_to_stage = {}
        with ApiClient(self.configuration) as client:
            all_jobs = client.jobs_api.list()[0]["results"]
            for jobs in all_jobs:
                if jobs["assignee"]:
                    if jobs["assignee"]["username"] == assignee:
                        job_id_to_stage[jobs["id"]] = jobs["stage"]
            for job_id, job_stage in job_id_to_stage.items():
                jobs_annotations = client.jobs_api.retrieve_annotations(job_id)
                jobs_annotations = jobs_annotations[0]["shapes"]
                bbox_count = len(jobs_annotations)
                bbox_total += bbox_count
                assignee_jobs_statistics.append(
                    {"job_id": job_id, "stage": job_stage, "bbox_count": bbox_count})

        return {"assignee": assignee, "bbox_total": bbox_total, "jobs": assignee_jobs_statistics}
