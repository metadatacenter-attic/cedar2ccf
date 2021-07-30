from string import punctuation
from stringcase import lowercase, snakecase

from rdflib import Graph, Namespace, URIRef, Literal, OWL
from rdflib.extras.infixowl import OWL_NS, Ontology, Class, Restriction,\
    Property, BooleanClass


class BSOntology:
    """CCF Biological Structure Ontology
    Represents the Biological Structure Ontology graph that can
    be mutated by supplying CEDAR metadata instances
    """
    _CCF_BASE_IRI = "http://purl.org/ccf/"

    _CCF_NS = Namespace(_CCF_BASE_IRI)
    _OBO_NS = Namespace("http://purl.obolibrary.org/obo/")
    _HGNC_NS = Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Hugo.owl#")

    def __init__(self, graph=None, **kwargs):
        self.graph = graph
        self.kwargs = kwargs

    @staticmethod
    def new():
        g = Graph()
        g.bind('ccf', BSOntology._CCF_NS)
        g.bind('obo', BSOntology._OBO_NS)
        g.bind('hgnc', BSOntology._HGNC_NS)
        g.bind('owl', OWL_NS)
        characterizing_biomarker_set =\
            Class(BSOntology._CCF_NS.characterizing_biomarker_set,
                  nameAnnotation=Literal("characterizing biomarker set"),
                  nameIsLabel=True,
                  graph=g)
        has_member =\
            Property(BSOntology._CCF_NS.has_member,
                     nameAnnotation=Literal("has member"),
                     nameIsLabel=True,
                     graph=g)
        located_in =\
            Property(BSOntology._OBO_NS.RO_0001025,
                     nameAnnotation=Literal("located in"),
                     nameIsLabel=True,
                     graph=g)
        cell_type_has_gene_marker =\
            Property(BSOntology._CCF_NS.cell_type_has_gene_marker,
                     nameAnnotation=Literal("cell type has gene marker"),
                     nameIsLabel=True,
                     graph=g)
        cell_type_has_protein_marker =\
            Property(BSOntology._CCF_NS.cell_type_has_protein_marker,
                     nameAnnotation=Literal("cell type has protein marker"),
                     nameIsLabel=True,
                     graph=g)
        is_biomarker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_biomarker_of_cell_type,
                     nameAnnotation=Literal("is biomarker of cell type"),
                     nameIsLabel=True,
                     graph=g)
        is_gene_marker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_gene_marker_of_cell_type,
                     subPropertyOf=[is_biomarker_of_cell_type],
                     nameAnnotation=Literal("is gene marker of cell type"),
                     nameIsLabel=True,
                     graph=g)
        is_protein_marker_of_cell_type =\
            Property(BSOntology._CCF_NS.is_protein_marker_of_cell_type,
                     subPropertyOf=[is_biomarker_of_cell_type],
                     nameAnnotation=Literal("is protein marker of cell type"),
                     nameIsLabel=True,
                     graph=g)
        cell_type_has_characterizing_biomarker_set =\
            Property(BSOntology._CCF_NS.cell_type_has_characterizing_biomarker_set,
                     nameAnnotation=Literal("cell type has characterizing biomarker set"),
                     nameIsLabel=True,
                     graph=g)
        is_characterizing_biomarker_set_of_cell_type =\
            Property(BSOntology._CCF_NS.is_characterizing_biomarker_set_of_cell_type,
                     nameAnnotation=Literal("is characterizing biomarkers of cell type"),
                     nameIsLabel=True,
                     graph=g)
        return BSOntology(
            g,
            ontology=Ontology(
                identifier=URIRef("http://purl.org/ccf/ccf-bso"),
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
            is_characterizing_biomarker_set_of_cell_type=is_characterizing_biomarker_set_of_cell_type)

    def mutate(self, instances):
        """
        """
        for instance in instances:
            anatomical_structure_iri =\
                instance['anatomical_structure']['@id']
            anatomical_structure_label =\
                instance['anatomical_structure']['rdfs:label']

            if self._CCF_BASE_IRI in anatomical_structure_iri:
                anatomical_structure =\
                    self._class(anatomical_structure_iri,
                                anatomical_structure_label)
                anatomical_structure.subClassOf =\
                    [self._class(self._OBO_NS.UBERON_0001062)]
            else:
                anatomical_structure = self._class(anatomical_structure_iri)

            cell_type_iri = instance['cell_type']['@id']
            cell_type_label = instance['cell_type']['rdfs:label']

            if self._CCF_BASE_IRI in cell_type_iri:
                cell_type = self._class(cell_type_iri, cell_type_label)
                cell_type.subClassOf = [self._class(self._OBO_NS.CL_0000000)]
            else:
                cell_type = self._class(cell_type_iri)

            cell_type.subClassOf =\
                [self._some_values_from(
                    self.kwargs['located_in'],
                    anatomical_structure)]

            characterizing_biomarker_set_label =\
                "characterizing biomarker set of " +\
                cell_type_label
            characterizing_biomarker_set_iri =\
                "http://purl.org/ccf/" +\
                snakecase(self._remove_punctuations(
                    lowercase(characterizing_biomarker_set_label)))

            characterizing_biomarker_set =\
                self._class(characterizing_biomarker_set_iri,
                            characterizing_biomarker_set_label)
            characterizing_biomarker_set.subClassOf =\
                [self.kwargs['characterizing_biomarker_set']]

            biomarkers = []
            for marker in instance['gene_biomarker']:
                if marker:
                    cls_gm = self._class(marker['@id'])
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
                    cls_pm = self._class(marker['@id'])
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
                        self._class(marker['@id'])) for marker in biomarkers],
                    graph=self.graph
                )]

            cell_type.subClassOf =\
                [self._some_values_from(
                    self.kwargs['cell_type_has_characterizing_biomarker_set'],
                    characterizing_biomarker_set)]

        return BSOntology(self.graph, **self.kwargs)

    def _class(self, iri, label=None):
        if label is not None:
            return Class(URIRef(iri),
                         nameAnnotation=Literal(label),
                         nameIsLabel=True,
                         graph=self.graph)
        else:
            return Class(URIRef(iri),
                         graph=self.graph)

    def _property(self, iri, label=None):
        if label is not None:
            return Property(URIRef(iri),
                            baseType=OWL.ObjectProperty,
                            nameAnnotation=Literal(label),
                            nameIsLabel=True,
                            graph=self.graph)
        else:
            return Property(URIRef(iri),
                            baseType=OWL.ObjectProperty,
                            graph=self.graph)

    def _attribute(self, iri, label=None):
        if label is not None:
            return Property(URIRef(iri),
                            baseType=OWL.DataProperty,
                            nameAnnotation=Literal(label),
                            nameIsLabel=True,
                            graph=self.graph)
        else:
            return Property(URIRef(iri),
                            baseType=OWL.DataProperty,
                            graph=self.graph)

    def _some_values_from(self, property, filler):
        return Restriction(property,
                           someValuesFrom=filler,
                           graph=self.graph)

    def _remove_punctuations(self, str):
        punctuation_excl_dash = punctuation.replace('-', '')
        return str.translate(str.maketrans('', '', punctuation_excl_dash))

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='turtle', destination=destination)
