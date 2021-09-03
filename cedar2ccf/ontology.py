from string import punctuation
from stringcase import lowercase, snakecase

from rdflib import Graph, Namespace, URIRef, Literal, OWL, RDFS
from rdflib.extras.infixowl import OWL_NS, Ontology, Class, Restriction,\
    Property, BooleanClass


class BSOntology:
    """CCF Biological Structure Ontology
    Represents the Biological Structure Ontology graph that can
    be mutated by supplying CEDAR metadata instances
    """
    _CCF_BASE_IRI = "http://purl.org/ccf/"

    _CCF_NS = Namespace(_CCF_BASE_IRI)
    _DC_TERMS_NS = Namespace("http://purl.org/dc/terms/")
    _OBO_NS = Namespace("http://purl.obolibrary.org/obo/")
    _HGNC_NS = Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Hugo.owl#")

    def __init__(self, graph=None, **kwargs):
        self.graph = graph
        self.kwargs = kwargs

    @staticmethod
    def new(ontology_iri):
        g = Graph()
        g.bind('ccf', BSOntology._CCF_NS)
        g.bind('dcterms', BSOntology._DC_TERMS_NS)
        g.bind('obo', BSOntology._OBO_NS)
        g.bind('hgnc', BSOntology._HGNC_NS)
        g.bind('owl', OWL_NS)
        characterizing_biomarker_set =\
            Class(BSOntology._CCF_NS.characterizing_biomarker_set, graph=g)
        has_member =\
            Property(BSOntology._CCF_NS.has_member, graph=g)
        located_in =\
            Property(BSOntology._OBO_NS.RO_0001025, graph=g)
        cell_type_has_gene_marker =\
            Property(BSOntology._CCF_NS.cell_type_has_gene_marker, graph=g)
        cell_type_has_protein_marker =\
            Property(BSOntology._CCF_NS.cell_type_has_protein_marker, graph=g)
        is_biomarker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_biomarker_of_cell_type, graph=g)
        is_gene_marker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_gene_marker_of_cell_type, graph=g)
        is_protein_marker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_protein_marker_of_cell_type, graph=g)
        cell_type_has_characterizing_biomarker_set =\
            Property(BSOntology._CCF_NS.cell_type_has_characterizing_biomarker_set,
                     graph=g)
        is_characterizing_biomarker_set_of_cell_type =\
            Property(BSOntology._CCF_NS.is_characterizing_biomarker_set_of_cell_type,
                     graph=g)
        source =\
            Property(BSOntology._DC_TERMS_NS.source,
                     baseType=OWL_NS.AnnotationProperty, graph=g)

        return BSOntology(
            g,
            ontology=Ontology(
                identifier=URIRef(ontology_iri),
                graph=g),
            characterizing_biomarker_set=characterizing_biomarker_set,
            has_member=has_member,
            located_in=located_in,
            cell_type_has_gene_marker=cell_type_has_gene_marker,
            cell_type_has_protein_marker=cell_type_has_protein_marker,
            is_biomarker_of_cell_type=is_biomarker_of_cell_type,
            is_gene_marker_of_cell_type=is_gene_marker_of_cell_type,
            is_protein_marker_of_cell_type=is_protein_marker_of_cell_type,
            cell_type_has_characterizing_biomarker_set=cell_type_has_characterizing_biomarker_set,
            is_characterizing_biomarker_set_of_cell_type=is_characterizing_biomarker_set_of_cell_type,
            source=source)

    def mutate(self, instances):
        """
        """
        for instance in instances:
            anatomical_structure_iri =\
                self._iri(instance['anatomical_structure']['@id'])

            if self._CCF_BASE_IRI in anatomical_structure_iri:
                anatomical_structure =\
                    self._class(anatomical_structure_iri)
                anatomical_structure.subClassOf =\
                    [self._class(self._OBO_NS.UBERON_0001062)]
            else:
                anatomical_structure = self._class(anatomical_structure_iri)

            cell_type_iri = self._iri(instance['cell_type']['@id'])

            if self._CCF_BASE_IRI in cell_type_iri:
                cell_type = self._class(cell_type_iri)
                cell_type.subClassOf = [self._class(self._OBO_NS.CL_0000000)]
            else:
                cell_type = self._class(cell_type_iri)

            cell_type.subClassOf =\
                [self._some_values_from(
                    self.kwargs['located_in'],
                    anatomical_structure)]

            characterizing_biomarker_set_label =\
                self._string("characterizing biomarker set of " +\
                             instance['cell_type']['rdfs:label'])
            characterizing_biomarker_set_iri =\
                self._iri(self._CCF_BASE_IRI + snakecase(
                    self._remove_punctuations(
                        lowercase(characterizing_biomarker_set_label))))

            characterizing_biomarker_set =\
                self._class(characterizing_biomarker_set_iri,
                            characterizing_biomarker_set_label)
            characterizing_biomarker_set.subClassOf =\
                [self.kwargs['characterizing_biomarker_set']]

            for doi in instance['doi']:
                doi_str = doi['@value']
                if doi_str is not None and "doi:" in doi_str:
                    self.graph.add((characterizing_biomarker_set.identifier,
                                   self.kwargs['source'].identifier,
                                   self._expand_doi(doi_str)))

            biomarkers = []
            for marker in instance['gene_biomarker']:
                if marker:
                    cls_gm = self._class(self._iri(marker['@id']))
                    cell_type.subClassOf =\
                        [self._some_values_from(
                            self.kwargs['cell_type_has_gene_marker'],
                            cls_gm)]
                    cls_gm.subClassOf =\
                        [self._some_values_from(
                            self.kwargs['is_gene_marker_of_cell_type'],
                            cell_type)]
                    biomarkers.append(marker)

            for marker in instance['protein_biomarker']:
                if marker:
                    cls_pm = self._class(self._iri(marker['@id']))
                    cell_type.subClassOf =\
                        [self._some_values_from(
                            self.kwargs['cell_type_has_protein_marker'],
                            cls_pm)]
                    cls_pm.subClassOf =\
                        [self._some_values_from(
                            self.kwargs['is_protein_marker_of_cell_type'],
                            cell_type)]
                    biomarkers.append(marker)

            characterizing_biomarker_set.equivalentClass =\
                [BooleanClass(
                    operator=OWL.intersectionOf,
                    members=[self._some_values_from(
                        self.kwargs['has_member'],
                        self._class(self._iri(marker['@id']))) for marker in biomarkers],
                    graph=self.graph
                )]

            cell_type.subClassOf =\
                [self._some_values_from(
                    self.kwargs['cell_type_has_characterizing_biomarker_set'],
                    characterizing_biomarker_set)]

        return BSOntology(self.graph, **self.kwargs)

    def _expand_doi(self, str):
        return URIRef(str.replace("doi:", "http://doi.org/"))

    def _class(self, identifier, label=None):
        c = Class(identifier, graph=self.graph)
        self._entity_label(c, label)
        return c

    def _property(self, identifier, label=None):
        p = Property(identifier, baseType=OWL.ObjectProperty, graph=self.graph)
        self._entity_label(p, label)
        return p

    def _attribute(self, identifier, label=None):
        a = Property(identifier, baseType=OWL.DataProperty, graph=self.graph)
        self._entity_label(a, label)
        return a

    def _entity_label(self, entity, label):
        if label is not None:
            self.graph.add((entity.identifier, RDFS.label, label))

    def _some_values_from(self, property, filler):
        return Restriction(property,
                           someValuesFrom=filler,
                           graph=self.graph)

    def _remove_punctuations(self, str):
        punctuation_excl_dash = punctuation.replace('-', '')
        return str.translate(str.maketrans('', '', punctuation_excl_dash))

    def _iri(self, str):
        return URIRef(str)

    def _string(self, str):
        return Literal(str)

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='application/rdf+xml',
                             destination=destination)
