import os
from cedar2ccf.client import CedarClient
from cedar2ccf.ontology import BSOntology


def run(args):
    """
    """
    with open(args.input_file, "r") as f:
        lines = [line.rstrip() for line in f]

    o = BSOntology.new(args.ontology_iri)
    for template_id in lines:
        user_id = os.getenv('CEDAR_USER_ID')
        api_key = os.getenv('CEDAR_API_KEY')

        client = CedarClient(user_id, api_key)
        instances = client.get_instances(is_based_on=template_id)
        o = o.mutate(instances)

    o.serialize(args.output)
