import logging
import sys


log = logging.getLogger(__name__)
log.setLevel("INFO")
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(handler)


class Jobs(object):

    def __init__(self, ml):

        assert ml

        self.ml = ml

    # TODO list by model?

    def list(self, minimal=True):
        """
        Queries the CloudML API, returning a dict of all jobs,
        keyed by job ID.

        If 'minimal' is specified, the state of each job will be returned,
        otherwise the full job metadata will be returned.

        :param minimal: returns only the job's state if set to True.

        :return: dict of job ID -> job information
        """
        result = self.ml.client.projects()\
            .jobs()\
            .list(parent="projects/{}".format(self.ml.project))\
            .execute()

        if minimal:
            return {j["jobId"]: j["state"] for j in result.get("versions", [])}
        return {j["jobId"]: j for j in result.get("versions", [])}

    def create(self):
        raise NotImplementedError()
