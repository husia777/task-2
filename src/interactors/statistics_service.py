

class StatisticsService:
    def __init__(self, cvat_facade) -> None:
        self.cvat_facade = cvat_facade

    def get_statistics_by_assignee(self, assignee: str):
        return self.cvat_facade.get_statistics_by_assignee(assignee)
