from tools.grits_record import FlightRecord, AirportRecord
from tools.csv_helpers import TabDialect, CommaDialect

from conf import settings

class FlightGlobalType(object):
    """ class that represents the .csv format of Flightglobal scheduled
    passenger and cargo flights

    NOTE: this report is used as the basis for the FlightRecord so the 'map_to'
    key is 1:1 with the schema key.
    """

    @property
    def map(self):
        return {
            'carrier' : { 'maps_to': 'carrier'},
            'flightnumber' : { 'maps_to': 'flightNumber'},
            'servicetype' : { 'maps_to': 'serviceType'},
            'effectivedate' : { 'maps_to': 'effectiveDate'},
            'discontinueddate' : { 'maps_to': 'discontinuedDate'},
            'day1' : { 'maps_to': 'day1'},
            'day2' : { 'maps_to': 'day2'},
            'day3' : { 'maps_to': 'day3'},
            'day4' : { 'maps_to': 'day4'},
            'day5' : { 'maps_to': 'day5'},
            'day6' : { 'maps_to': 'day6'},
            'day7' : { 'maps_to': 'day7'},
            'departureairport' : { 'maps_to': 'departureAirport'},
            'departurecity' : { 'maps_to': 'departureCity'},
            'departurestate' : { 'maps_to': 'departureState'},
            'departurecountry' : { 'maps_to': 'departureCountry'},
            'departuretimepub' : { 'maps_to': 'departureTimePub'},
            'departuretimeactual' : { 'maps_to': 'departureTimeActual'},
            'departureutcvariance' : { 'maps_to': 'departureUTCVariance'},
            'departureterminal' : { 'maps_to': 'departureTerminal'},
            'arrivalairport' : { 'maps_to': 'arrivalAirport'},
            'arrivalcity' : { 'maps_to': 'arrivalCity'},
            'arrivalstate' : { 'maps_to': 'arrivalState'},
            'arrivalcountry' : { 'maps_to': 'arrivalCountry'},
            'arrivaltimepub' : { 'maps_to': 'arrivalTimePub'},
            'arrivaltimeactual' : { 'maps_to': 'arrivalTimeActual'},
            'arrivalutcvariance' : { 'maps_to': 'arrivalUTCVariance'},
            'arrivalterminal' : { 'maps_to': 'arrivalTerminal'},
            'subaircraftcode' : { 'maps_to': 'subAircraftCode'},
            'groupaircraftcode' : { 'maps_to': 'groupAircraftCode'},
            'classes' : { 'maps_to': 'classes'},
            'classesfull' : { 'maps_to': 'classesFull'},
            'trafficrestriction' : { 'maps_to': 'trafficRestriction'},
            'flightarrivaldayindicator' : { 'maps_to': 'flightArrivalDayIndicator'},
            'stops' : { 'maps_to': 'stops'},
            'stopcodes' : { 'maps_to': 'stopCodes'},
            'stoprestrictions' : { 'maps_to': 'stopRestrictions'},
            'stopsubaircraftcodes' : { 'maps_to': 'stopsubAircraftCodes'},
            'aircraftchangeindicator' : { 'maps_to': 'aircraftChangeIndicator'},
            'meals' : { 'maps_to': 'meals'},
            'flightdistance' : { 'maps_to': 'flightDistance'},
            'elapsedtime' : { 'maps_to': 'elapsedTime'},
            'layovertime' : { 'maps_to': 'layoverTime'},
            'inflightservice' : { 'maps_to': 'inFlightService'},
            'ssimcodesharestatus' : { 'maps_to': 'SSIMcodeShareStatus'},
            'ssimcodesharecarrier' : { 'maps_to': 'SSIMcodeShareCarrier'},
            'codeshareindicator' :  { 'maps_to': 'codeshareIndicator'},
            'wetleaseindicator' : { 'maps_to': 'wetleaseIndicator'},
            'codeshareinfo' : { 'maps_to': 'codeshareInfo'},
            'wetleaseinfo' : { 'maps_to': 'wetleaseInfo'},
            'operationalsuffix' : { 'maps_to': 'operationalSuffix'},
            'ivi' : { 'maps_to': 'ivi'},
            'leg' : { 'maps_to': 'leg'},
            'recordid' : { 'maps_to': 'recordId'},
            'daysofoperation' : { 'maps_to': 'daysOfOperation'},
            'totalfrequency' : { 'maps_to': 'totalFrequency'},
            'weeklyfrequency' : { 'maps_to': 'weeklyFrequency'},
            'availseatmi' : { 'maps_to': 'availSeatMi'},
            'availseatkm' : { 'maps_to': 'availSeatKm'},
            'intstoparrivaltime' : { 'maps_to': 'intStopArrivaltime'},
            'intstopdeparturetime' : { 'maps_to': 'intStopDepartureTime'},
            'intstopnextday' : { 'maps_to': 'intStopNextDay'},
            'physicallegkey' : { 'maps_to': 'physicalLegKey'},
            'departureairportname' : { 'maps_to': 'departureAirportName'},
            'departurecityname' : { 'maps_to': 'departureCityName'},
            'departurecountryname' : { 'maps_to': 'departureCountryName'},
            'arrivalairportname' : { 'maps_to': 'arrivalAirportName'},
            'arrivalcityname' : { 'maps_to': 'arrivalCityName'},
            'arrivalcountryname' : { 'maps_to': 'arrivalCountryName'},
            'aircrafttype' : { 'maps_to': 'aircraftType'},
            'carriername' : { 'maps_to': 'carrierName'},
            'totalseats' : { 'maps_to': 'totalSeats'},
            'firstclassseats' : { 'maps_to': 'firstClassSeats'},
            'businessclassseats' : { 'maps_to': 'businessClassSeats'},
            'premiumeconomyclassseats' : { 'maps_to': 'premiumEconomyClassSeats'},
            'economyclassseats' : { 'maps_to': 'economyClassSeats'},
            'aircrafttonnage' : { 'maps_to': 'aircraftTonnage'}}

    def __init__(self):
        """ FlightGlobalType constructor

        Describes the 'contract' for the report, such as the positional
        processing rules.
        """
        self.collection_name = settings._FLIGHT_COLLECTION_NAME # name of the MongoDB collection
        self.record = FlightRecord
        # positional processing rules
        self.title_position = None # zero-based position of the record set title
        self.header_position = 0 # zero-based position of the record set header
        self.data_position = 1 # zero-based position of the record set
        self.num_empty_rows_eod = 0 # data runs until end of file
        self.dialect=CommaDialect()

class DiioAirportType(object):
    """ class that represents the .tsv format of Diio Mi Express 'Airport'
    report """

    @property
    def map(self):
        return { 'code': { 'maps_to': 'code'},
        'name': { 'maps_to': 'name'},
        'city': { 'maps_to': 'city'},
        'state': { 'maps_to': 'state'},
        'state name':{ 'maps_to': 'stateName'},
        'longitude': { 'maps_to': 'longitude'},
        'latitude': { 'maps_to': 'latitude'},
        'country': { 'maps_to': 'country'},
        'country name': { 'maps_to': 'countryName'},
        'global region': { 'maps_to': 'globalRegion'},
        'wac': { 'maps_to': 'WAC'},
        'notes': { 'maps_to': 'notes'}}

    def __init__(self):
        """ AirportType constructor

        Describes the 'contract' for the report, such as the positional
        processing rules.
        """
        self.collection_name = settings._AIRPORT_COLLECTION_NAME # name of the MongoDB collection
        self.record = AirportRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set Longitude' in record:
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 0 # data runs until end of file
        self.dialect=TabDialect()
