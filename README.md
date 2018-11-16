# Business Analyst Utilities

I use the tools and data shipped with ArcGIS Business Analyst _a lot_ as part of my data preperation pipelines. However, working with these resources in Python is not always the easiest. To streamline some of this, I have created a few tools taking advantage of reading the registry entries to access some of the more useful resources I find myself frequently needing to quickly access.

## Data

The main thing I've implmented thus far is referencing the data resources, notably the address locators, network dataset, parent directory where the data is stored, and the respective geographies as layers. Accessing the address locator, network dataset and parent directory properties will return a string path to these resources.


