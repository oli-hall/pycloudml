import logging
import sys

from googleapiclient.errors import HttpError

from pycloudml.errors import NoSuchModelException

log = logging.getLogger(__name__)
log.setLevel("INFO")
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(handler)


class Model(object):
    """
    Class to wrap a selection of utility methods for querying/updating
    a CloudML Model.

    Currently, this will raise an Exception if the model does not exist
    during any method call.
    """

    def __init__(self, ml, model_name):

        assert ml
        assert model_name

        self.ml = ml
        self.model_name = model_name

        if not self.exists():
            raise NoSuchModelException("Model '{}' does not exist".format(model_name))

    def exists(self):
        """
        Checks if the model exists.

        :return: boolean, True if model exists, False otherwise.
        """
        try:
            self.ml.client.projects().models().get(
                name=self._full_model_name(self.ml.project, self.model_name)
            ).execute()
            return True
        except HttpError as e:
            if e.resp["status"] == "404":
                return False
            raise e

    @staticmethod
    def _full_model_name(project_id, model_name):
        """
        Converts a model name to the full format.

        Full format:

        projects/<project_id>/models/<model_name>

        :param project_id: GCP Project ID
        :param model_name: model name
        :return: the full model name
        """
        assert project_id
        assert model_name

        return "/projects/{}/models/{}".format(project_id, model_name)

    def status(self):
        """
        Returns the current state of the default version of the model.

        :return: string, model state
        """
        info = self.info()
        return info["defaultVersion"]["state"]

    def info(self):
        """
        Returns the full model information.

        :return: dict, model information
        """
        try:
            return self.ml.client.projects().models().get(
                name=self._full_model_name(self.ml.project, self.model_name)
            ).execute()
        except HttpError as e:
            if e.resp["status"] == "404":
                raise NoSuchModelException("'{}' does not exist".format(self.model_name))
            raise e

    def versions(self):
        """
        TODO
        """
        raise NotImplementedError()

    def patch(self):
        """
        TODO
        """
        raise NotImplementedError()

    def delete(self):
        """
        Deletes the model.

        :return: the (dict) results of the deletion
        """
        log.info("Deleting model {}...".format(self.model_name))
        try:
            return self.ml.client.projects().models().delete(
                name=self._full_model_name(self.ml.project, self.model_name)
            ).execute()
        except HttpError as e:
            if e.resp["status"] == "404":
                raise NoSuchModelException("'{}' does not exist".format(self.model_name))
            raise e
