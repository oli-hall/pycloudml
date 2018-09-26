import time

from googleapiclient.errors import HttpError

from pycloudml.model import Model
from pycloudml.errors import ModelAlreadyExistsException
import logging
import sys


log = logging.getLogger(__name__)
log.setLevel("INFO")
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(handler)


class Versions(object):

    def __init__(self, ml, model_name):

        assert ml
        assert model_name

        self.ml = ml
        self.model_name = model_name

    def list(self, minimal=True):
        """
        Queries the CloudML API, returning a dict of all versions for a particular model,
        keyed by version name.

        If 'minimal' is specified, the state of each version will be returned,
        otherwise the full version metadata will be returned.

        :param minimal: returns only the version's state if set to True.

        :return: dict of version name -> version information
        """
        result = self.ml.client.models()\
            .versions()\
            .list(parent="projects/{}/models/{}".format(self.ml.project, self.model_name))\
            .execute()

        if minimal:
            return {self._simplify(v["name"]): v["state"] for v in result.get("versions", [])}
        return {self._simplify(v["name"]): v for v in result.get("versions", [])}

    @staticmethod
    def _simplify(project_id, model_name, version_name):
        """
        If version name is full format, simplifies it and returns it.

        Full format:

        projects/<project_id>/models/<model_name>/versions/<version_name>

        :param project_id: GCP Project ID
        :param model_name: model name
        :param version_name: version name to simplify
        :return: the simplified version name
        """
        assert project_id
        assert model_name
        assert version_name

        prefix = "projects/{}/models/{}/versions".format(project_id, model_name)
        if prefix not in version_name:
            return version_name
        return version_name.replace(prefix, "")

    # TODO add flag to set as default once created
    def create(self, version_name, description=None, online_prediction_logging=False,
               labels=None):
        """Creates a CloudML model with the provided settings, returning a Model
        object representing the created model.

        :param version_name: the name of the version
        :param description: the (optional) description of the model (default: None)
        :param online_prediction_logging: whether to enable StackDriver logging for
        online prediction (default: False)
        :param labels: a dict of (key:value) labels to tag the model with (default: None)
        :return: Model object
        """
        raise NotImplementedError()
        log.info("Creating version '{}'".format(version_name))

        model_data = {
            "name": version_name,
            "regions": [
                self.ml.region
            ],
            "onlinePredictionLogging": online_prediction_logging,
        }

        if description:
            model_data["description"] = description

        if labels is not None:
            # TODO verify that labels is dict
            model_data["labels"] = labels

        log.debug("Model settings: {}".format(model_data))

        try:
            result = self.ml.client.projects().models().create(
                parent="projects/{}/models/{}".format(self.ml.project, self.model_name),
                body=model_data
            ).execute()
        except HttpError as e:
            if e.resp["status"] == "409":
                raise ModelAlreadyExistsException("Model '{}' already exists".format(version_name))
            raise e

        log.debug("Create call for model '{}' returned: {}".format(version_name, result))

        model = Model(self.ml, version_name)

        log.info("Model '{}' is ready.".format(version_name))
        return model
