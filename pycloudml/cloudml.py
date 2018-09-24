from googleapiclient import discovery

from pycloudml.model import Model
from pycloudml.models import Models


class CloudML(object):
    """
    Wraps a CloudML client and region/project information, giving a
    single point to interact with Models, Jobs and Operations.
    """

    def __init__(self, project, region='europe-west1'):
        self.client = self._get_client()
        self.project = project
        self.region = region

    def _get_client(self):
        """Builds a client to the CloudML API."""
        return discovery.build('ml', 'v1')

    def models(self, model_name=None):
        """
        Allows the user to interact with a specific model or all
        models (depending upon whether model_name is specified).

        If model_name is specified, but there is no model with
        that name, raises a NoSuchModelException

        :param model_name: string, name of model to fetch (optional)
        :return: Model/Models
        """
        if model_name:
            return Model(self, model_name)

        return Models(self)

    def jobs(self, job_id=None):
        """
        Allows the user to interact with a specific job or all
        jobs (depending upon whether job_id is specified).

        If job_id is specified, but there is no job with
        that job ID, raises a NoSuchJobException

        :param job_id: string, ID of job to fetch (optional)
        :return: Job/Jobs
        """
        if job_id:
            return Job(self, job_id)

        return Jobs(self)
