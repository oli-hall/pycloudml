import logging
import sys

from googleapiclient.errors import HttpError

from pycloudml.errors import NoSuchJobException

log = logging.getLogger(__name__)
log.setLevel("INFO")
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(handler)


class Job(object):
    """
    Class to wrap a selection of utility methods for querying/updating
    a CloudML Job.

    Currently, this will raise an Exception if the job does not exist
    during any method call.
    """

    def __init__(self, ml, job_id):

        assert ml
        assert job_id

        self.ml = ml
        self.job_id = job_id

        if not self.exists():
            raise NoSuchJobException("Job '{}' does not exist".format(job_id))

    def exists(self):
        """
        Checks if the job exists.

        :return: boolean, True if job exists, False otherwise.
        """
        try:
            self.info()
            return True
        except NoSuchJobException:
            return False

    @staticmethod
    def _full_job_name(project_id, job_id):
        """
        Converts a job ID to the full format.

        Full format:

        projects/<project_id>/jobs/<job_id>

        :param project_id: GCP Project ID
        :param job_id: job ID
        :return: the full job name
        """
        assert project_id
        assert job_id

        return "projects/{}/jobs/{}".format(project_id, job_id)

    def status(self):
        """
        Returns the current state of the job.

        :return: string, job state
        """
        info = self.info()
        return info["state"]

    def info(self):
        """
        Returns the full job information.

        :return: dict, job information
        """
        try:
            return self.ml.client.projects()\
                .jobs()\
                .get(
                    name=self._full_job_name(self.ml.project, self.job_id)
                ).execute()
        except HttpError as e:
            if e.resp["status"] == "404":
                raise NoSuchJobException("Job '{}' does not exist".format(self.job_id))
            raise e

    def patch(self):
        """
        TODO
        """
        raise NotImplementedError()

    def cancel(self):
        """
        TODO
        """
        raise NotImplementedError()

    def delete(self):
        """
        Deletes the Job.

        :return: the (dict) results of the deletion
        """
        log.info("Deleting job {}...".format(self.job_id))
        try:
            return self.ml.client.projects()\
                .jobs()\
                .delete(
                    name=self._full_job_name(self.ml.project, self.job_id)
                ).execute()
        except HttpError as e:
            if e.resp["status"] == "404":
                raise NoSuchJobException("'{}' does not exist".format(self.job_id))
            raise e
