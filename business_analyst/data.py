# import modules
import sys
import os
import re
from arcgis.features import GeoAccessor
import arcpy

if sys.version_info > (3, 0):
    import winreg
else:
    import _winreg as winreg


class Data:

    def __init__(self):
        pass

    @staticmethod
    def _get_child_keys(key_path):
        """
        Get the full path of first generation child keys under the parent key listed.
        :param key_path: Path to the parent key in registry.
        :return: List of the full path to child keys.
        """
        # open the parent key
        parent_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

        # variables to track progress and store results
        error = False
        counter = 0
        key_list = []

        # while everything is going good
        while not error:

            try:
                # get the child key in the iterated position
                child_key = winreg.EnumKey(parent_key, counter)

                # add the located key to the list
                key_list.append('{}\\{}'.format(key_path, child_key))

                # increment the counter
                counter += 1

            # when something blows up...typically because no key is found
            except Exception as e:

                # switch the error flag to true, stopping the iteration
                error = True

        # give the accumulated list back
        return key_list

    def _get_first_child_key(self, key_path, pattern):
        """
        Based on the pattern provided, find the key with a matching string in it.
        :param key_path: Full string path to the key.
        :param pattern: Pattern to be located.
        :return: Full path of the first key path matching the provided pattern.
        """
        # get a list of paths to keys under the parent key path provided
        key_list = self._get_child_keys(key_path)

        # iterate the list of key paths
        for key in key_list:

            # if the key matches the pattern
            if key.find(pattern):
                # pass back the provided key path
                return key

    @property
    def _usa_key(self):
        """
        Get the key for the current data installation of Business Analyst data.
        :return: Key for the current data installation of Business Analyst data.
        """
        return self._get_first_child_key('Software\ESRI\BusinessAnalyst\Datasets', 'USA_ESRI')

    def _get_business_analyst_key_value(self, locator_key):
        """
        In the Business Analyst key, get the value corresponding to the provided locator key.
        :param locator_key: Locator key.
        :return: Key value.
        """
        # open the key to the current installation of Business Analyst data
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self._usa_key)

        # query the value of the locator key
        return winreg.QueryValueEx(key, locator_key)[0]

    @property
    def usa_locator(self):
        """
        Path to the address locator installed with Business Analyst USA data.
        :return: String directory path to the address locator installed with Business Analyst USA data.
        """
        return self._get_business_analyst_key_value('Locator')

    @property
    def usa_network_dataset(self):
        """
        Path to the network dataset installed with Business Analyst USA data.
        :return: String directory path to the network dataset installed with Business Analyst USA data.
        """
        return self._get_business_analyst_key_value('StreetsNetwork')

    @property
    def usa_data_path(self):
        """
        Path where the Business Analyst USA data is located.
        :return: String directory path to where the Business Analyst USA data is installed.
        """

        return self._get_business_analyst_key_value('DataInstallDir')

    def _create_demographic_layer(self, feature_class_name, layer_name):
        """
        Esri Business Analyst standard geography layer with ID and NAME fields.
        :param feature_class_path: Name of the feature class.
        :param layer_name: Output layer name.
        :return: Feature Layer
        """
        # get the path to the geodatabase where the Esri demographics reside
        demographic_dir = os.path.join(self.usa_data_path, 'Data', 'Demographic Data')
        gdb_name = [d for d in os.listdir(demographic_dir) if re.match(r'USA_ESRI_\d{4}\.gdb', d)][0]
        gdb_path = os.path.join(demographic_dir, gdb_name)
        fc_path = os.path.join(gdb_path, feature_class_name)

        # create layer map
        visible_fields = ['Shape', 'ID', 'NAME']

        def eval_visible(field_name):
            if field_name in visible_fields:
                return 'VISIBLE'
            else:
                return 'HIDDEN'

        field_map_lst = [' '.join([f.name, f.name, eval_visible(f.name), 'NONE']) for f in arcpy.ListFields(fc_path)]
        field_map = ';'.join(field_map_lst)

        # create and return the feature layer
        return arcpy.management.MakeFeatureLayer(fc_path, field_info=field_map)[0]

    @property
    def layer_block_group(self):
        """
        Esri Business Analyst Census Block Group layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('BlockGroups_bg', 'block_group')

    @property
    def layer_cbsa(self):
        """
        Esri Business Analyst CBSA layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('CBSAs_cb', 'cbsa')

    @property
    def layer_census_tract(self):
        """
        Esri Business Analyst Census Tract layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('CensusTracts_tr', 'census_tract')

    @property
    def layer_congressional_district(self):
        """
        Esri Business Analyst Congressional District layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('CongressionalDistricts_cd', 'congressional_district')

    @property
    def layer_county(self):
        """
        Esri Business Analyst county layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('Counties_cy', 'county')

    @property
    def layer_county_subdivisions(self):
        """
        Esri Business Analyst county subdivision layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('CountySubdivisions_cs', 'county_subdivision')

    @property
    def layer_dma(self):
        """
        Esri Business Analyst DMA layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('DMAs_dm', 'dma')

    @property
    def layer_places(self):
        """
        Esri Business Analyst Census Places layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('Places_pl', 'places')

    @property
    def layer_states(self):
        """
        Esri Business Analyst US States layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('States_st', 'state')

    @property
    def layer_postal_code(self):
        """
        Esri Business Analyst postal code (zip) layer with ID and NAME fields.
        :return: Feature Layer
        """
        return self._create_demographic_layer('ZIPCodes_zp', 'postal_code')

# create instance of data for use
data = Data()

@property
def to_sdf(self):
    # convert the layer to a spatially enabled dataframe
    df = GeoAccessor.from_featureclass(self)

    # get rid of the object id field and return the dataframe
    return df.drop('OBJECTID', axis=1)


# now, monkeypatch this onto the layer object
arcpy._mp.Layer.sdf = to_sdf