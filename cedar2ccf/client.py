from urllib.parse import quote_plus
from cedar2ccf.utils import json_handler


class CedarClient:
    """CEDAR API client
    Provides functions to easily access the CEDAR API
    (https://resource.metadatacenter.org/api/) in Python.

    Attributes:
        get_instances: Retrieves CEDAR metadata instances given the
        template id.
    """

    _BASE_URL = "https://resource.metadatacenter.org"
    _SEARCH = "search"
    _TEMPLATE_INSTANCES = "template-instances"
    _VERSION = "version"
    _IS_BASED_ON = "is_based_on"
    _LIMIT = "limit"
    _OFFSET = "offset"

    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key

    def get_instances(self, is_based_on, limit=None):
        """Returns all CEDAR metadata instances given the template id.

        Args:
            is_based_on (str): An IRI string representing the template id.
            limit (int): (Optional) An integer indicating the maximum number
                of returned instances.

        Returns:
            An object containing the instances with the given template id.
        """
        instances = []
        for instance_id in self._get_instance_ids(is_based_on, limit):
            identifier = quote_plus(instance_id)
            url = f"{self._BASE_URL}/{self._TEMPLATE_INSTANCES}/{identifier}"
            response = json_handler(url, self.api_key)
            instances.append(response)

        return instances

    def _get_instance_ids(self, is_based_on, limit=None):
        """
        """
        params = f"{self._VERSION}=latest&{self._IS_BASED_ON}={is_based_on}"
        if (limit):
            params = f"{params}&{self._LIMIT}={limit}"

        url = f"{self._BASE_URL}/{self._SEARCH}?{params}"

        response = json_handler(url, self.api_key)

        instance_ids = []
        for resource in response["resources"]:
            instance_ids.append(resource["@id"])

        return instance_ids

