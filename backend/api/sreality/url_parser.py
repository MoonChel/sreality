from typing import List, Dict
from urllib.parse import urlparse, parse_qsl
from .api_query import api_query, city_to_region
from pprint import pprint


def find_by_value(key: str, values: List[str]) -> Dict[str, str]:
    result = {}

    for k, v in api_query[key].items():
        for vv in values:
            if v == vv:
                result[k] = vv

    return result


def url_parser(url: str):
    # url = "https://www.sreality.cz/hledani/prodej/byty/brno?pois_in_place_distance=2&pois_in_place=2&navic=balkon&velikost=3%2Bkk,2%2Bkk,2%2B1,3%2B1&vlastnictvi=osobni&stav=velmi-dobry-stav&patro-od=1&patro-do=10&plocha-od=20&plocha-do=100&cena-od=0&cena-do=6000000"

    url_parsed = urlparse(url)
    query_parsed = dict(parse_qsl(url_parsed.query))

    api_params = {
        "locality_country_id": "112",
    }

    # byty, domy...
    for i, t in api_query["category_main_cb"].items():
        if t in url_parsed.path:
            api_params["category_main_cb"] = i
            break

    # prodej, pronajem...
    for i, t in api_query["category_type_cb"].items():
        if t in url_parsed.path:
            api_params["category_type_cb"] = i
            break

    # brno, plzen...
    for i, t in api_query["locality_district_id"].items():
        if t in url_parsed.path:
            api_params["locality_district_id"] = i
            api_params["locality_region_id"] = city_to_region[i]
            break

    # parse velikost
    velikost = query_parsed.get("velikost")
    if velikost:
        # 1+kk, les, mobilni domek
        category_sub_cb_set = set(api_query["category_sub_cb"].values())

        items = set(velikost.split(","))

        if items.issubset(category_sub_cb_set):
            k = "category_sub_cb"
            api_params[k] = "|".join(find_by_value(k, items).keys())

        # 1-pokoj, 2-pokoje
        room_count_cb_set = set(api_query["room_count_cb"].values())

        if items.issubset(room_count_cb_set):
            k = "room_count_cb"
            api_params[k] = find_by_value(k, items).keys()

    # parse vlastnictvi
    vlastnictvi = query_parsed.get("vlastnictvi")
    if vlastnictvi:
        k = "ownership"
        api_params[k] = "|".join(find_by_value(k, vlastnictvi.split(",")).keys())

    # parse stav
    stav = query_parsed.get("stav")
    if stav:
        k = "building_condition"
        api_params[k] = find_by_value(k, stav.split(","))

    # parse plocha-od
    plocha_od = query_parsed.get("plocha-od")
    k = "usable_area"
    if plocha_od:
        api_params[k] = plocha_od
    else:
        api_params[k] = "0"

    # parse plocha-do
    plocha_do = query_parsed.get("plocha-do")
    if plocha_do:
        k = "usable_area"
        api_params[k] += "|" + plocha_do

    # parse cena-od
    cena_od = query_parsed.get("cena-od")
    k = "czk_price_summary_order2"
    if cena_od:
        api_params[k] = cena_od
    else:
        api_params[k] = "0"

    # parse cena-do
    cena_do = query_parsed.get("cena-do")
    if cena_do:
        k = "czk_price_summary_order2"
        api_params[k] += "|" + cena_do

    # parse patro-od
    patro_od = query_parsed.get("patro-od")
    k = "floor_number"
    if patro_od:
        api_params[k] = patro_od
    else:
        api_params[k] = "0"

    # parse patro-do
    patro_do = query_parsed.get("patro-do")
    if patro_do:
        k = "floor_number"
        api_params[k] += "|" + patro_do

    return api_params


if __name__ == "__main__":
    u = url_parser()
    pprint(u)
