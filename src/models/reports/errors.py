class ReportError(Exception):
    def __init__(self, message):
        self.message = message


class EmptyReportException(ReportError):
    pass
