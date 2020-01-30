import json
from urllib import request
from urllib.parse import urlencode
from dbhelper import postgres_handler
from settings import SerpstatConf, log


def serpstat_get_keywords(domain: str, search_engine: str, user_id: int):
    """
    :param user_id:
    :param domain: domain name that you want to get information of
    :param search_engine: search engine name
    :return:
    """
    method = 'domain_info'
    params = {
        'query': domain,  # string for get info
        'se': search_engine,  # string search engine
        'token': postgres_handler.get_user_key(user_id)['api_key'],  # string personal token
    }
    api_url = f'{SerpstatConf.HOST}/{method}?{urlencode(params)}'
    try:
        json_data = request.urlopen(api_url).read()
        return json.loads(json_data)
    except Exception as e0:
        log.error("API request error: {error}".format(error=e0))


def serpstat_get_limits(user_id: int):
    method = 'stats'
    params = {
        'token': postgres_handler.get_user_key(user_id)['api_key'],  # string personal token
    }
    api_url = f'{SerpstatConf.HOST}/{method}?{urlencode(params)}'
    try:
        json_data = request.urlopen(api_url).read()
        return json.loads(json_data)
    except Exception as e0:
        log.error("API request error: {error}".format(error=e0))


def serpstat_databases_info():
    method = 'databases_info'
    params = {
        'token': 'c0d0ec831b48b7e0ee783ede81dba592',  # string personal token
    }
    api_url = f'{SerpstatConf.HOST}/{method}?{urlencode(params)}'
    try:
        json_data = request.urlopen(api_url).read()
        return json.loads(json_data)
    except Exception as e0:
        log.error("API request error: {error}".format(error=e0))


def plain_domain(domain: str, search_engine: str, user_id: int):
    serpstat_result = serpstat_get_keywords(domain, search_engine, user_id)
    if serpstat_result['result']:
        return serpstat_result['result']['keywords'], serpstat_result['result']['traff']
    else:
        return serpstat_result['status_msg'], serpstat_result['status_msg']


def api_key_limit(user_id: int):
    serpstat_result = serpstat_get_limits(user_id)
    if serpstat_result['status_msg'] == 'Invalid token!':
        return 'Invalid token!'
    return serpstat_result['result']['left_lines']


if __name__ == '__main__':
    print(serpstat_databases_info())
    # for se in ['y_213', 'g_ru']:
    #     print(plain_domain('tt365.ru', se))
