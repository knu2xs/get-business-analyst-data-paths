# Get Business Analyst Data Paths Tools

Business Analyst data includes a network dataset for routing and an address locator for geocoding. When building scripts needing to take advantage of this capability, typically you have to assume the default installation path, or you have to have the user input this as an input parameter. Inputting this when running a script or tool is annoying at best, and sometimes even impossible for an end user who may  not even know what to look for or where to look.

Fortunately Python can read from the Windows Registry, and the paths to these resources are saved in the Registry. This module provides two functions reading the location of resources from the registry, and returning the full file path to find them on the local machine. One function is provided for the USA composite address locator, `get_usa_locator_path`, and another for the network data set, `get_usa_network_dataset_path`.

Use is pretty simple, just import and use with no parameters.

```
# import modules
from get_business_analyst_data_paths import get_usa_locator_path

# get the path to the USA address locator
address_locator = get_usa_locator_path()

# now go write the rest of the script and geocode like a champ!
```

```
# import modules
from get_business_analyst_data_paths import get_usa_network_dataset_path

# get the path to the USA address locator
network_dataset = get_usa_network_dataset_path()

# now go write the rest of the script and route like a boss!
```