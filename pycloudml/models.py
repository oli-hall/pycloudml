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


class Models(object):

    def __init__(self, ml):

        assert ml

        self.ml = ml

    def list(self, minimal=True):
        """
        Queries the CloudML API, returning a dict of all models,
        keyed by model name.

        If 'minimal' is specified, the state of each model's default version will be returned,
        otherwise the full model metadata will be returned.

        :param minimal: returns only the model's state if set to True.

        :return: dict of model name -> model information
        """
        result = self.ml.client.models()\
            .list(parent="projects/".format(self.ml.project))\
            .execute()

        if minimal:
            return {self._simplify(c["name"]): c["defaultVersion"]["state"]
                    for c in result.get("models", [])}
        return {self._simplify(c["name"]): c for c in result.get("models", [])}

    @staticmethod
    def _simplify(project_id, model_name):
        """
        If model name is full format, simplifies it and returns it.

        Full format:

        projects/<project_id>/models/<model_name>

        :param project_id: GCP Project ID
        :param model_name: model name
        :return: the simplified model name
        """
        assert project_id
        assert model_name

        prefix = "projects/{}/models/".format(project_id)
        if prefix not in model_name:
            return model_name
        return model_name.replace(prefix, "")

    def create(self, model_name, description=None, online_prediction_logging=False,
               labels=None):
        """Creates a CloudML model with the provided settings, returning a Model
        object representing the created model.

        :param model_name: the name of the model
        :param description: the (optional) description of the model (default: None)
        :param online_prediction_logging: whether to enable StackDriver logging for
        online prediction (default: False)
        :param labels: a dict of (key:value) labels to tag the model with (default: None)
        :return: Model object
        """
        log.info("Creating model '{}'".format(model_name))

        model_data = {
            "name": model_name,
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
                parent="projects/{}".format(self.ml.project),
                body=model_data
            ).execute()
        except HttpError as e:
            if e.resp["status"] == "409":
                raise ModelAlreadyExistsException("Model '{}' already exists".format(model_name))
            raise e

        log.debug("Create call for model '{}' returned: {}".format(model_name, result))

        model = Model(self.ml, model_name)

        log.info("Model '{}' is ready.".format(model_name))
        return model
