import os

from rdflib import Graph, Namespace, URIRef
from rdflib.extras.infixowl import Class, Restriction, Property

from pycedar.convert.owl import *
import pycedar.CedarClient

user_id = os.getenv('CEDAR_USER_ID')
api_key = os.getenv('CEDAR_API_KEY')

client = CedarClient(user_id, api_key)

instances = client.get_instances(
        is_based_on='some template id',
        limit='an integer or blank')

ccf = Namespace('http://purl.org/ccf/')
obo = Namespace('http://purl.obolibrary.org/obo/')

g = Graph()
g.bind('', 'http://purl.org/ccf/')
g.bind('ccf', 'http://purl.org/ccf/')
g.bind('obo', 'http://purl.obolibrary.org/obo/')
g.bind('hgnc', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Hugo.owl#')

part_of = Property(obo.BFO_0000050, graph=g)
located_in = Property(obo.RO_0001025, graph=g)
cell_has_gene_marker = Property(ccf.CCF_0000052, graph=g)
cell_has_protein_marker = Property(ccf.CCF_0000053, graph=g)
cell_has_proteoform_marker = Property(ccf.CCF_0000054, graph=g)
cell_has_lipid_marker = Property(ccf.CCF_0000055, graph=g)
cell_has_metabolite_marker = Property(ccf.CCF_0000056, graph=g)
biomarker_characterizes_cell = Property(ccf.CCF_0000057, graph=g)

for instance in instances:
    anatomical_structure = URIRef(instance['anatomical_structure']['@id'])
    cell_type = URIRef(instance['cell_type']['@id'])
    c = Class(anatomical_structure, graph=g)
    c.subClassOf = [Restriction(located_in, graph=g, someValuesFrom=cell_type)]

    for marker in instance['gene_biomarker']:
        gene_marker = URIRef(marker['@id'])
        c = Class(cell_type, graph=g)
        c.subClassOf = [Restriction(cell_has_gene_marker, graph=g, someValuesFrom=gene_marker)]

g.serialize(format='turtle', destination="ccf-bso.ttl")
