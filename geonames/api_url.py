#!/usr/bin/env python
"""
This file collects all the different api endpoints and constructs the urls.
"""

from urllib.parse import urlencode
from datetime import date

__author__ = "Dawud Hage"
__copyright__ = "Copyright 2017"
__credits__ = ["Dawud Hage"]
__license__ = "MIT"
__version__ = "0"
__maintainer__ = "Dawud Hage"
__email__ = "me@dawudhage.com"
__status__ = "Prototype"


class APIUrl(object):
    def __init__(self, username, secure=True, default_output_format="JSON"):
        """
        
        :param username: The registered username at geonames.org, register here: http://www.geonames.org/login
        :type username: str
        :param secure: True for using the secure endpoint
        :type secure: bool
        :param default_output_format: The default output format of the api ('JSON' or 'XML')
        :type default_output_format: str
        """

        assert isinstance(username, str), "parameter username must be of type str"
        assert isinstance(secure, bool), "parameter secure must be of type bool"
        assert default_output_format in ["JSON", "XML"], "default_output_format can only be 'JSON' or 'XML'."

        self.username = username
        self._base_url = self._create_base_url(secure)
        self.default_output_format = default_output_format

    def search(self, q=None, name=None, name_equals=None, name_starts_with=None, max_rows=None, start_row=None,
               country=None, country_bias=None, continent_code=None, admin_code1=None, admin_code2=None,
               admin_code3=None,
               feature_class=None, feature_code=None, cities=None, language=None, style=None, is_name_required=None,
               tag=None, operator=None, charset=None, fuzzy=None, north=None, east=None, south=None, west=None,
               search_language=None, order_by=None, include_bbox=None, secure=None, output_format=None):
        """
        This function implements the full-text search api, see: http://www.geonames.org/export/geonames-search.html
        :param q: search over all attributes of a place : place name, country name, continent, admin codes,... 
        :type q: str
        :param name: place name 
        :type name: str
        :param name_equals: exact place name
        :type name_equals: str
        :param name_starts_with: place name starts with given characters
        :type name_starts_with: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 100, the maximal allowed value is 1000.
        :type max_rows: int
        :param start_row: Used for paging results. If you want to get results 30 to 40, use startRow=30 and maxRows=10. 
         Default is 0, the maximal allowed value is 5000 for the free services and 25000 for the premium services
        :type start_row: int
        :param country: Default is all countries. The country parameter may occur more than once
        :type country: str or list
        :param country_bias: records from the countryBias are listed first (2 letter country code, ISO-3166)
        :type country_bias: str
        :param continent_code: restricts the search for toponym of the given continent: AF,AS,EU,NA,OC,SA,AN.
        :type continent_code: str
        :param admin_code1: code of administrative subdivision
        :type admin_code1: str
        :param admin_code2: code of administrative subdivision
        :type admin_code2: str
        :param admin_code3: code of administrative subdivision
        :type admin_code3: str
        :param feature_class: featureclass(es): A,H,L,P,R,S,T,U,V, see: http://www.geonames.org/export/codes.html
        :type feature_class: str or list
        :param feature_code: featurecode(s), see: http://www.geonames.org/export/codes.html
        :type feature_code: str or list
        :param cities: optional filter parameter with three possible values 'cities1000', 'cities5000','cities15000' 
         used to categorize the populated places into three groups according to size/relevance.
        :type cities: str
        :param language: place name and country name will be returned in the specified language. Default is English.
         Feature classes and codes are only available in English and Bulgarian. ISO-636 2-letter language code; en,de,..
        :type language: str
        :param style: verbosity of returned xml document, default = MEDIUM: SHORT,MEDIUM,LONG,FULL
        :type style: str
        :param is_name_required: At least one of the search term needs to be part of the place name. 
         Example : A normal search for Berlin will return all places within the state of Berlin. 
         If we only want to find places with 'Berlin' in the name we set the parameter isNameRequired to 'true'. 
         The difference to the name_equals parameter is that this will allow searches for 'Berlin, Germany' 
         as only one search term needs to be part of the name.
        :type is_name_required: bool
        :param tag: search for toponyms tagged with the specified tag 
        :type tag: str
        :param operator: default is 'AND', with the operator 'OR' not all search terms need to be matched
        :type operator: str
        :param charset: default is 'UTF8', defines the encoding used for the document returned by the web service.
        :type charset: str
        :param fuzzy: default is '1', defines the fuzziness of the search terms. float between 0 and 1. 
         The search term is only applied to the name attribute. 
        :type fuzzy: float
        :param north: bounding box, only features within the box are returned
        :type north: float
        :param east: bounding box, only features within the box are returned
        :type east: float
        :param south: bounding box, only features within the box are returned
        :type south: float
        :param west: bounding box, only features within the box are returned
        :type west: float
        :param search_language: in combination with the name parameter, the search will only consider names in the 
         specified language. Used for instance to query for IATA airport codes.
        :type search_language: str
        :param order_by: in combination with the name_startsWith, if set to 'relevance' than the result is sorted by 
         relevance. can be one of: population,elevation,relevance
        :type order_by: str
        :param include_bbox: include Bbox info, regardelss of style setting. (normally only included with style=FULL
         is a string 'true'
        :type include_bbox: str
        
        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML', 'RDF'
        :type output_format: str
        
        :return: The corresponding url
        :rtype: str
        """

        # Check if the required parameters are given
        assert any((q, name, name_equals)), "q, name or name_equals required"

        if secure:
            base_url = self._create_base_url(secure)
        else:
            base_url = self._base_url

        # Add the search endpoint:
        url = base_url + "search?"
        keys = [("username", self.username)]

        self._add_key_value(keys, key='q', value=q)
        self._add_key_value(keys, key='name', value=name)
        self._add_key_value(keys, key='name_equals', value=name_equals)
        self._add_key_value(keys, key='name_startsWith', value=name_starts_with)
        self._add_key_value(keys, key='maxRows', value=max_rows)
        self._add_key_value(keys, key='startRow', value=start_row)
        if country is not None:
            if isinstance(country, str):
                country = [country]
            for c in country:
                self._add_key_value(keys, key='country', value=c)
        self._add_key_value(keys, key='countryBias', value=country_bias)
        self._add_key_value(keys, key='continentCode', value=continent_code)
        self._add_key_value(keys, key='adminCode1', value=admin_code1)
        self._add_key_value(keys, key='adminCode2', value=admin_code2)
        self._add_key_value(keys, key='adminCode3', value=admin_code3)
        if feature_class is not None:
            if isinstance(feature_class, str):
                feature_class = [feature_class]
            for f in feature_class:
                self._add_key_value(keys, key='featureClass', value=f)
        if feature_code is not None:
            if isinstance(feature_code, str):
                feature_code = [feature_code]
            for f in feature_code:
                self._add_key_value(keys, key='featureCode', value=f)
        self._add_key_value(keys, key='cities', value=cities)
        self._add_key_value(keys, key='lang', value=language)
        self._add_key_value(keys, key='style', value=style)
        self._add_key_value(keys, key='isNameRequired', value=is_name_required)
        self._add_key_value(keys, key='tag', value=tag)
        self._add_key_value(keys, key='operator', value=operator)
        self._add_key_value(keys, key='charset', value=charset)
        self._add_key_value(keys, key='fuzzy', value=fuzzy)
        if None not in (north, east, south, west):
            self._add_key_value(keys, key='north', value=north)
            self._add_key_value(keys, key='east', value=east)
            self._add_key_value(keys, key='south', value=south)
            self._add_key_value(keys, key='west', value=west)
        self._add_key_value(keys, key='searchlang', value=search_language)
        self._add_key_value(keys, key='orderby', value=order_by)
        self._add_key_value(keys, key='inclBbox', value=include_bbox)
        if output_format is None:
            output_format = self.default_output_format
        self._add_key_value(keys, key='type', value=output_format)

        return url + urlencode(keys, encoding="utf-8")

    # # Places
    def cities_and_place_names_bounding_box(self, north, east, south, west, language=None,
                                            max_rows=None, secure=None, output_format=None):
        """
        Implementation of the Cities and Placenames api, the url will result in:
         returns a list of cities and placenames in the bounding box, ordered by relevancy (capital/population). 
         Placenames close together are filterered out and only the larger name is included in the resulting list.

        :param north: bounding box, only features within the box are returned
        :type north: float
        :param east: bounding box, only features within the box are returned
        :type east: float
        :param south: bounding box, only features within the box are returned
        :type south: float
        :param west: bounding box, only features within the box are returned
        :type west: float
        :param language: language of placenames and wikipedia urls (default = en)
        :type language: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 10
        :type max_rows: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "cities", output_format)

        # assert the required parameters
        assert None not in (north, east, south, west), "north, east, south and west are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='north', value=north)
        self._add_key_value(keys, key='east', value=east)
        self._add_key_value(keys, key='south', value=south)
        self._add_key_value(keys, key='west', value=west)

        # Add the optional parameter:
        self._add_key_value(keys, key='lang', value=language)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    # # Place Hierarchy
    def children(self, geoname_id, hierarchy=None, max_rows=None, secure=None, output_format=None):
        """
        Implementation of the Children api, the url will result in:
          Returns the children (admin divisions and populated places) for a given geonameId. 
          The children are the administrative divisions within an other administrative division, 
          like the counties (ADM2) in a state (ADM1) or also the countries in a continent. 
          The leafs are populated places, other feature classes like spots, mountains etc are not included 
          in this service. Use the search service if you need other feature classes as well.

        :param geoname_id: the geonameId of the parent
        :type geoname_id: int
        :param hierarchy: this optional parameter allows to use other hiearchies then the default administrative 
         hierarchy. So far only 'tourism' is implemented.
        :type hierarchy: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 200
        :type max_rows: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "children", output_format)

        assert geoname_id, "geoname_id is a required parameter."

        self._add_key_value(keys, key='geonameId', value=geoname_id)
        self._add_key_value(keys, key='hierarchy', value=hierarchy)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    def neighbours(self, geoname_id=None, country=None, secure=None, output_format=None):
        """
        Implementation of the Neighbours api, the url will result in:
          Returns all neighbours for a country or administrative division. 
          (coverage: all countries on country level, and lower levels as specified here: 
          http://www.geonames.org/export/subdiv-level.html)
          returns the neighbours of a toponym, currently only implemented for countries

        :param geoname_id: the geonameId of the parent
        :type geoname_id: int
        :param country: the country code (alternative parameter instead of the geonameId)
        :type country: str

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "neighbours", output_format)

        assert any((geoname_id, country)) and not all((geoname_id, country)), \
            "geoname_id or country is a required parameter."

        self._add_key_value(keys, key='geonameId', value=geoname_id)
        self._add_key_value(keys, key='country', value=country)

        return url + urlencode(keys, encoding="utf-8")

    def hierarchy(self, geoname_id, secure=None, output_format=None):
        """
        Implementation of the Hierarchy api, the url will result in:
          Returns all GeoNames higher up in the hierarchy of a place name. 
          returns a list of GeoName records, ordered by hierarchy level. 
          The top hierarchy (continent) is the first element in the list 

        :param geoname_id: the geonameId for the hierarchy
        :type geoname_id: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "hierarchy", output_format)

        assert geoname_id, "geoname_id is a required parameter."

        self._add_key_value(keys, key='geonameId', value=geoname_id)

        return url + urlencode(keys, encoding="utf-8")

    def siblings(self, geoname_id, secure=None, output_format=None):
        """
        Implementation of the Siblings api, the url will result in:
          Returns all siblings of a GeoNames toponym with feature class A.
          returns a list of GeoNames records (feature class A) 
          that have the same administrative level and the same father 

        :param geoname_id: the geonameId for the hierarchy
        :type geoname_id: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "siblings", output_format)

        assert geoname_id, "geoname_id is a required parameter."

        self._add_key_value(keys, key='geonameId', value=geoname_id)

        return url + urlencode(keys, encoding="utf-8")

    # # Postal codes
    def postal_code_to_place_name(self, postal_code, country=None, charset=None, max_rows=None, secure=None,
                                  output_format=None):
        """
        Implementation of the Placename lookup with postalcode api, the url will result in:
          returns a list of places for the given postalcode, sorted by postalcode,placename 

        :param postal_code: The postalcode of interest
        :type postal_code: int or str
        :param country: Default is all countries.
        :type country: str
        :param charset: default is 'UTF-8', defines the encoding used for the document returned by the web service.
        :type charset: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 20
        :type max_rows: int
        
        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "postalCodeLookup", output_format)

        assert postal_code, "postal_code is a required parameter."

        self._add_key_value(keys, key='postalcode', value=postal_code)
        self._add_key_value(keys, key='country', value=country)
        self._add_key_value(keys, key='charset', value=charset)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    def wikipedia_find_nearby(self, latitude=None, longitude=None, postal_code=None, radius=None, language=None,
                              max_rows=None, country=None, secure=None, output_format=None):
        """
        Implementation of the Find nearby Wikipedia Entries api, the url will result in:
         returns a list of wikipedia entries. Either the latitud + longitude or the postal code is required.

        :param latitude: The latitude of interest
        :type latitude: float
        :param longitude: The longitude of interest
        :type longitude: float
        :param postal_code: The postalcode of interest
        :type postal_code: int or str
        :param radius: buffer in km for closest timezone in coastal areas
        :type radius: int
        :param language: language code, see http://www.geonames.org/wikipedia.html (default = en)
        :type language: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 5
        :type max_rows: int
        :param country: Default is all countries.
        :type country: str

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "findNearbyWikipedia", output_format)

        # assert the required parameters
        if postal_code is None:
            assert latitude is not None and longitude is not None, \
                "Either (latitude + longitude) OR postal_code should be provided."
        else:
            assert (latitude is None or longitude is None), \
                "Only (latitude + longitude) OR postal_code should be provided."

        # Add the optional parameter:
        self._add_key_value(keys, key='lat', value=latitude)
        self._add_key_value(keys, key='lng', value=longitude)
        self._add_key_value(keys, key='postalcode', value=postal_code)
        self._add_key_value(keys, key='radius', value=radius)
        self._add_key_value(keys, key='lang', value=language)
        self._add_key_value(keys, key='maxRows', value=max_rows)
        self._add_key_value(keys, key='country', value=country)

        return url + urlencode(keys, encoding="utf-8")

    def wikipedia_fulltext_search(self, q, title=None, language=None, max_rows=None, secure=None, output_format=None):
        """
        Implementation of the Wikipedia Fulltext Search api, the url will result in:
         returns the wikipedia entries found for the searchterm
         
        :param q: place name
        :type q: str
        :param title: search in the wikipedia title (optional)
        :type title: str
        :param language: language code, see http://www.geonames.org/wikipedia.html (default = en)
        :type language: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 10
        :type max_rows: int
        
        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str
        
        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "wikipediaSearch", output_format)

        # assert the required parameters
        assert q, "q is a required parameter."

        # Add the required parameters
        self._add_key_value(keys, key='q', value=q)

        # Add the optional parameter:
        self._add_key_value(keys, key='title', value=title)
        self._add_key_value(keys, key='lang', value=language)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    def wikipedia_bounding_box(self, north, east, south, west, language=None,
                               max_rows=None, secure=None, output_format=None):
        """
        Implementation of the Wikipedia Articles in Bounding Box api, the url will result in:
         returns the wikipedia entries within the bounding bo

        :param north: bounding box, only features within the box are returned
        :type north: float
        :param east: bounding box, only features within the box are returned
        :type east: float
        :param south: bounding box, only features within the box are returned
        :type south: float
        :param west: bounding box, only features within the box are returned
        :type west: float
        :param language: language code, see http://www.geonames.org/wikipedia.html (default = en)
        :type language: str
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 5
        :type max_rows: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "wikipediaBoundingBox", output_format)

        # assert the required parameters
        assert all((north, east, south, west)), "north, east, south and west are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='north', value=north)
        self._add_key_value(keys, key='east', value=east)
        self._add_key_value(keys, key='south', value=south)
        self._add_key_value(keys, key='west', value=west)

        # Add the optional parameter:
        self._add_key_value(keys, key='lang', value=language)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    # # Earthquakes: http://www.geonames.org/export/JSON-webservices.html#earthquakesJSON
    def earthquakes_bounding_box(self, north, east, south, west, up_to_date=None, min_magnitude=None, max_rows=None,
                                 secure=None, output_format=None):
        """
        Implementation of the Weather Stations with most recent Weather Observation api, the url will result in:
         returns a list of weather stations with the most recent weather observation

        :param north: bounding box, only features within the box are returned
        :type north: float
        :param east: bounding box, only features within the box are returned
        :type east: float
        :param south: bounding box, only features within the box are returned
        :type south: float
        :param west: bounding box, only features within the box are returned
        :type west: float
        :param up_to_date: date of earthquakes, earthquakes older or equal the given date sorted by date, magnitude
        :type up_to_date: datetime.date or str "YYYY-MM-DD"
        :param min_magnitude: the minimal magnitude
        :type min_magnitude: int
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 10
        :type max_rows: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "earthquakes", output_format)

        # assert the required parameters
        assert all((north, east, south, west)), "north, east, south and west are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='north', value=north)
        self._add_key_value(keys, key='east', value=east)
        self._add_key_value(keys, key='south', value=south)
        self._add_key_value(keys, key='west', value=west)

        # Add the optional parameter:
        self._add_key_value(keys, key='minMagnitude', value=min_magnitude)
        self._add_key_value(keys, key='maxRows', value=max_rows)

        self._add_date(keys, up_to_date)

        return url + urlencode(keys, encoding="utf-8")

    # # Weather: http://www.geonames.org/export/JSON-webservices.html#weatherJSON
    def weather_station_bounding_box(self, north, east, south, west, max_rows=None, secure=None, output_format=None):
        """
        Implementation of the Weather Stations with most recent Weather Observation api, the url will result in:
         returns a list of weather stations with the most recent weather observation

        :param north: bounding box, only features within the box are returned
        :type north: float
        :param east: bounding box, only features within the box are returned
        :type east: float
        :param south: bounding box, only features within the box are returned
        :type south: float
        :param west: bounding box, only features within the box are returned
        :type west: float
        :param max_rows: the maximal number of rows in the document returned by the service. Default is 10
        :type max_rows: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "weather", output_format)

        # assert the required parameters
        assert all((north, east, south, west)), "north, east, south and west are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='north', value=north)
        self._add_key_value(keys, key='east', value=east)
        self._add_key_value(keys, key='south', value=south)
        self._add_key_value(keys, key='west', value=west)

        # Add the optional parameter:
        self._add_key_value(keys, key='maxRows', value=max_rows)

        return url + urlencode(keys, encoding="utf-8")

    def weather_station_icao(self, icao, secure=None, output_format=None):
        """
        Implementation of the Weather Stations with most recent Weather Observation api, the url will result in:
         returns the weather station and the most recent weather observation for the ICAO code

        :param icao: International Civil Aviation Organization (ICAO) code 
        :type icao: str

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "weatherIcao", output_format)

        # assert the required parameters
        assert icao, "icao is a required parameter."

        # Add the required parameters
        self._add_key_value(keys, key='ICAO', value=icao)

        return url + urlencode(keys, encoding="utf-8")

    def weather_station_find_nearby(self, latitude, longitude, radius=None, secure=None, output_format=None):
        """
        Implementation of the Weather Station with most recent weather observation  api, the url will result in:
         returns a weather station with the most recent weather observation
         
        :param latitude: The latitude of interest
        :type latitude: float
        :param longitude: The longitude of interest
        :type longitude: float
        :param radius: search radius, only weather stations within this radius are considered. Default is about 100km.
        :type radius: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "findNearByWeather", output_format)

        # assert the required parameters
        assert latitude or longitude, "latitude and longitude are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='lat', value=latitude)
        self._add_key_value(keys, key='lng', value=longitude)

        # Add the optional parameter:
        self._add_key_value(keys, key='radius', value=radius)

        return url + urlencode(keys, encoding="utf-8")

    # # Other webservices
    def country_info(self, country=None, language=None, secure=None, output_format=None):
        """
        Implementation of the Country Info api, the url will result in:
         Country information : Capital, Population, Area in square km, Bounding Box of mainland 
         (excluding offshore islands)

        :param country: Default is all countries, accepts multiple countries.
        :type country: str or list
        :param language: language code (ISO-639-1), (default = en)
        :type language: str

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, accepts: 'JSON', and 'CSV'
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "countryInfo", output_format, additional_output_formats="CSV")

        # Add the optional parameter:
        if country is not None:
            if isinstance(country, str):
                country = [country]
            for c in country:
                self._add_key_value(keys, key='country', value=c)
        self._add_key_value(keys, key='lang', value=language)

        return url + urlencode(keys, encoding="utf-8")

    def ocean(self, latitude, longitude, radius=None, secure=None, output_format=None):
        """
        Implementation of the Ocean api, the url will result in:
         returns the ocean or sea for the given latitude/longitude The oceans returned by the service are listed here:
         http://www.geonames.org/export/ocean.html

        :param latitude: The latitude of interest
        :type latitude: float
        :param longitude: The longitude of interest
        :type longitude: float
        :param radius: buffer in km
        :type radius: int

        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML',
        :type output_format: str

        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "ocean", output_format)

        # assert the required parameters
        assert latitude or longitude, "latitude and longitude are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='lat', value=latitude)
        self._add_key_value(keys, key='lng', value=longitude)

        # Add the optional parameter:
        self._add_key_value(keys, key='radius', value=radius)

        return url + urlencode(keys, encoding="utf-8")

    def timezone(self, latitude, longitude, radius=None, language=None, sunrise_sunset_date=None, secure=None,
                 output_format=None):
        """
        Implementation of the timezone api, the url will result in:
        the timezone at the lat/lng with gmt offset (1. January) and dst offset (1. July) 
        
        :param latitude: The latitude of interest
        :type latitude: float
        :param longitude: The longitude of interest
        :type longitude: float
        :param radius: buffer in km for closest timezone in coastal areas
        :type radius: int
        :param language: The language for the country name
        :type language: str
        :param sunrise_sunset_date: date to give sunrise/sunset times
        :type sunrise_sunset_date: datetime.date or str "YYYY-MM-DD"
        
        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML',
        :type output_format: str
        
        :return: The corresponding url
        :rtype: str
        """

        url, keys = self._create_bare_end_point(secure, "timezone", output_format)

        # assert the required parameters
        assert latitude or longitude, "latitude and longitude are required parameters."

        # Add the required parameters
        self._add_key_value(keys, key='lat', value=latitude)
        self._add_key_value(keys, key='lng', value=longitude)

        # Add the optional parameter:
        self._add_key_value(keys, key='radius', value=radius)
        self._add_key_value(keys, key='lang', value=language)
        self._add_date(keys, sunrise_sunset_date)

        return url + urlencode(keys, encoding="utf-8")

    # # Private methods
    @staticmethod
    def _create_base_url(secure):
        """
        Depending if a secure connection is desired the endpoint changes
        :param secure: True for using the secure endpoint
        :return: a base endpoint as a string
        """
        if secure:
            return "https://secure.geonames.org/"
        # Do not use the secure endpoint
        return "http://api.geonames.org/"

    def _create_bare_end_point(self, secure, end_point, output_format=None, additional_output_formats=None):
        """
        Create a base endpoint that is needed for most methods
        
        :param secure: Overwrite the class parameter secure, True for using the secure endpoint
        :type secure: bool
        :param output_format: Overwrite the class parameter default_output_format, 'JSON', 'XML',
        :type output_format: str
        :param additional_output_formats: Additional output format to add for this endpoint,
        :type additional_output_formats: str or list
        
        :return: url, keys
        :rtype: str, list of 2 element-tuples
        """
        if secure:
            base_url = self._create_base_url(secure)
        else:
            base_url = self._base_url

        # Add the search endpoint:
        url = base_url + end_point
        if output_format:
            if output_format.upper() == "JSON":
                url += "JSON"
            if additional_output_formats is not None:
                if isinstance(additional_output_formats, str):
                    additional_output_formats = [additional_output_formats]
                additional_output_formats = [f.upper() for f in additional_output_formats]
            if output_format.upper() == "CSV" and output_format.upper() in additional_output_formats:
                url += "CSV"
        else:
            if self.default_output_format == "JSON":
                url += "JSON"
        url += "?"

        keys = [("username", self.username)]

        return url, keys

    @staticmethod
    def _add_key_value(keys, key, value):
        """
        This function adds a key-value pair to the keys list, if the value is None it will not be added.
        :param keys: The key-value pairs that will be used to construct the API url
        :type keys: list
        :param key: The key to add
        :type key: str
        :param value: The value belonging to the key
        """
        if value is not None:
            keys.append((key, str(value)))

    def _add_date(self, keys, date_to_add, key='date'):
        """
        This function adds a key-value date pair to the keys list, if the date_to_add is None it will not be added.
        :param keys: The key-value pairs that will be used to construct the API url
        :type keys: list
        :param date_to_add: The value belonging to the key
        :type date_to_add: datetime.date or str "YYYY-MM-DD"
        :param key: The key to add, defaults='date'
        :type key: str
        """

        if isinstance(date_to_add, date):
            date_to_add = date_to_add.strftime("%Y-%m-%d")

        self._add_key_value(keys, key, date_to_add)


if __name__ == "__main__":
    a = APIUrl('API_KEY')
    print(a.search(q='Düsseldorf', country=["DE", "NL"], feature_code='AIRP'))
    print(a.timezone(51.2277, 6.7735, sunrise_sunset_date=date(year=2017, month=7, day=7)))
    print(a.search(q='costa del sol'))
    print(a.wikipedia_fulltext_search(q="Düsseldorf", language="NL", output_format="XML"))
    print(a.wikipedia_find_nearby(postal_code=40545, country="DE"))
    print(a.wikipedia_bounding_box(north=44.1, south=-9.9, east=-22.4, west=55.2))
    print(a.search(q='Indonesia', feature_class='T'))
    print(a.weather_station_bounding_box(north=44.1, south=-9.9, east=-22.4, west=55.2))
    print(a.postal_code_to_place_name(postal_code="8935PJ", country="NL"))
    print(a.ocean(52.008544, 4.093947))
    print(a.ocean(51.995504, 4.121587))
    print(a.country_info(['NL', 'DE']))
    print(a.neighbours(country='DE'))
    print(a.neighbours(geoname_id=2782113))
