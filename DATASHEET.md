## DATASHEET FOR NORMAN PD DATA


### For what purpose was the dataset created?
This dataset was created as part of the Data Engineering Assignment. 

### Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description.
The task is to address the gap between raw police incident data and its usefulness for further analysis by enriching it with contextual details like weather and location.
This provides further information to better analyze the Incident data.

### Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?
Created By: Vaishnavi Madireddy

Affiliation: University of Florida

## What data does each instance consist of?
Each record represents a single police incident report. Each instance contains:
##### Time of the incident report
##### Textual description of the location of the incident 
##### Unique identifier for the incident report
##### Text description of the type of incident reported
##### Incident ORI

### “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description.
The initial data  comes from raw text within police incident PDFs


### Is any information missing from individual instances?
Certain Instances do not contain Location, Nature or even ORI. This is missing from the Raw data i.e, it is missing in PDFs.

### Are relationships between individual instances made explicit?
In this dataset, relationships between individual incidents aren't explicitly modeled.However, there might be implicit connections. For instance, consistent location details across reports could indicate related incidents in the same area, or similar incident types ("nature") might hint at a broader pattern.


### Are there any errors, sources of noise, or redundancies in the dataset?
The data exhibits inconsistencies and missing information that require cleaning. Some columns contain extraneous characters like punctuation or typos. Additionally, a substantial number of addresses (around XX%, if possible quantify) are labelled "Nearby" based on coordinates, suggesting potential inconsistencies in location recording. Furthermore, some entries lack location data entirely.

### Is the dataset self-contained, or does it link to or otherwise rely on external resources ?
Yes the data set is self contained.

### Does the dataset contain data that might be considered confidential?
No this dataset does not contain any confidential data.

### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?
No this dataset does not contain any such data.

### Does the dataset relate to people?
This dataset indirectly relates to people.The data seems to focus on police incident reports, not directly on people. This incidents does invole people. 


### Collection Process

### Was the data directly observable (e.g., raw text, movie ratings), reported by subjects (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part-of-speech tags, model-based guesses for age or language)? If data was reported by subjects or indirectly inferred/derived from other data, was the data validated/verified? If so, please describe how.
Inferred/derived from text (police reports). Verification unknown, possibly partially verified or internally checked.

### What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)?
The police incident reports themselves probably originated from a law enforcement agency's system. This system likely uses software or APIs to collect and store the incident data electronically.
Further parsing is performed on multiple PDF files.


### Were any ethical review processes conducted (e.g., by an institutional review board)?
N/A

### Does the dataset relate to people?
Not Directly.


### Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?
Assignment 0 module involved writing code to extract data from PDFs. This involved parsing text and populating the initial dataset, suggesting some level of pre-processing.

### Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?
No, it was not saved

### Is the software used to preprocess/clean/label the instances available?
N/A



### Has the dataset been used for any tasks already?
N/A

### Is there a repository that links to any or all papers or systems that use the dataset?
N/A

### What (other) tasks could the dataset be used for?
Incident Classification, Clustering, Anomaly Detection

### Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created?
N/A

### How will the dataset will be distributed (e.g., tarball on website, API, GitHub)?
N/A

### Does the dataset have a digital object identifier (DOI)?
N/A

### Any other comments?
The Augmented data contains further information supporting the dataset.
