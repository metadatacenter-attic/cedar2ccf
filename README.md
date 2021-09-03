# CEDAR-to-CCF

A Python tool to convert CEDAR metadata instances to CCF Biological Structure Ontology.

The CCF Biological Structure Ontology (CCF-BSO) models the relationship between a human cell type and its characterizing biomarkers. Each anatomical structure in the human body consists of different cell types and the same cell types might exist in multiple organ locations. The CCF-BSO makes the distinction between the cell types that are found in several locations by naming them differently, for example, the 'fibroblast' cell has various names such as "fibroblast of anterior cardiac vein", "fibroblast of coronary sinus", "fibroblast of epicardium", etc. The distinction is important in developing a human atlas because those cells may inherit different properties, such as their characterizing biomarkers.

The creation of the CCF-BSO starts by working with organ experts to manually construct the relevant partonomies of anatomical structure and describe the cell types present in the anatomical structure by presenting a set of their characterizing biomarkers (e.g., gene, protein, lipid and metabolite expression profiles). Additionally, the experts may add some publication DOIs that contain the conclusion about the cell type and its biomarkers. These acquired metadata are then converted into OWL axioms which are the building blocks of the CCF-BSO.

## Acquiring the metadata using CEDAR and converting them to OWL axioms

The organ experts will use CEDAR during the data collection. Our team at Stanford has developed several metadata templates to accomodate the data collection for different major human organs (e.g., brain, heart, kidney, lung, etc.). The figure below shows an example of CEDAR metadata instance.

<img width="600" alt="Screen Shot 2021-08-05 at 12 26 50 PM" src="https://user-images.githubusercontent.com/5062950/128409356-b12d953d-6001-4cbc-bc8b-86df4f9af984.png">

CEDAR stores metadata instances in JSON-LD format and users are able to access their data on the Web via REST API. This Python tool utilizes this feature to convert the CEDAR metadata instances into OWL axioms to construct the CCF-BSO.

<img width="950" alt="Screen Shot 2021-07-28 at 3 59 36 PM" src="https://user-images.githubusercontent.com/5062950/128410465-0a711e2f-3911-4639-9bdb-3996f1857c9b.png">

## Installing the tool

You can install the application using `pip` after you clone the repository.
```
$ cd cedar2ccf
$ pip install .
```

## Using the tool

1. Set up the environment variables. Follow the instructions [on this site](https://metadatacenter.github.io/cedar-manual/advanced_topics/b2_cedars_api/) to retrieve the CEDAR API key from your account.
   ```
   export CEDAR_USER_ID=<your-cedar-user-id>
   export CEDAR_API_KEY=<your-cedar-api-key>
   ```

2. Create a text file containing a list of HuBMAP organ template IDs on CEDAR. You may need to request access to the HuBMAP project team to get these template IDs.
   ```
   $ vi templates.txt 
   ```

3. Run the tool
   ```
   $ cedar2ccf templates.txt --ontology-iri http://purl.org/ccf/data/asctb.owl -o asctb.owl
   ```

4. Open the resulting output file using [Protégé](https://protege.stanford.edu/)

   <img width="950" alt="Screen Shot 2021-08-05 at 12 53 31 PM" src="https://user-images.githubusercontent.com/5062950/128412602-d0666515-a325-4d1e-b778-914e941bed36.png">
