"""
filters wrappers for betfair api
"""
import json

def to_camel_case(snake_str):
    """
    Converts snake_string to camelCase
    :param str snake_str:
    :returns: str
    """
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])

def market(event_type_ids=None, competition_ids=None, event_ids=None, market_ids=None,
           market_type_codes=None, attributes=None):
    """
    :param list event_type_ids: filter market data by eventTypeIds.
    :param list competition_ids: filter market data by competitionIds.
    :param list event_ids: filter market data by eventIds.
    :param list market_ids: filter market data by marketIds.
    :param list market_type_codes: filter market data by marketTypeCodes.
    :param dict attributes: additional query attributes outside of filter.

    :return: json
    """
    args = locals().copy()
    del args['attributes']
    query_filter = dict()
    if attributes:
        query_filter = {to_camel_case(k): v for k, v in attributes.items()}
    query_filter['filter'] = {to_camel_case(k): v for k, v in args.items() if v is not None}

    return json.dumps(query_filter)
