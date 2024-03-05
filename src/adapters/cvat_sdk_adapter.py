from abc import ABC, abstractmethod
from cvat_sdk.api_client import Configuration, ApiClient
from cvat_sdk.core.helpers import get_paginated_collection


class CVATSdkFacadeInterface(ABC):
    @abstractmethod
    def get_statistics_by_assignee(self, assignee: str):
        pass


class CVATSdkFacade(CVATSdkFacadeInterface):
    configuration = Configuration(host="http://192.168.13.20:8080/", username='hnaimov',
                                  password='Lr3&qQvA',)

    def get_statistics_by_assignee(self, assignee: str):
        bbox_total = 0
        assignee_jobs_statistics = []
        job_id_to_stage = {}
        assignee_projects_id = []
        assignee_tasks_id = []
        with ApiClient(self.configuration) as client:
            all_jobs = get_paginated_collection(
                client.jobs_api.list_endpoint)
            all_tasks = get_paginated_collection(
                client.tasks_api.list_endpoint)
            all_projects = get_paginated_collection(
                client.projects_api.list_endpoint)

            for project in all_projects:
                if project["assignee"]:

                    if project["assignee"]["username"] == assignee:
                        assignee_projects_id.append(project["id"])

            for task in all_tasks:
                if task["assignee"]:
                    if task["assignee"]["username"] == assignee:
                        assignee_tasks_id.append(task["id"])
            for job in all_jobs:
                if job["assignee"]:
                    if job["assignee"]["username"] == assignee:
                        job_id_to_stage[job["id"]] = job["stage"]
                elif job["project_id"] in assignee_projects_id:
                    job_id_to_stage[job["id"]] = job["stage"]

                elif job["task_id"] in assignee_tasks_id:
                    job_id_to_stage[job["id"]] = job["stage"]

            for job_id, job_stage in job_id_to_stage.items():
                jobs_annotations = client.jobs_api.retrieve_annotations(job_id)
                jobs_annotations = jobs_annotations[0]["shapes"]
                bbox_count = len(jobs_annotations)
                bbox_total += bbox_count
                assignee_jobs_statistics.append(
                    {"job_id": job_id, "stage": job_stage, "bbox_count": bbox_count})
        return {"assignee": assignee, "bbox_total": bbox_total, "jobs": assignee_jobs_statistics}
