import math
import asyncio
import unicodedata

from typing import Tuple, List, Dict, Optional

import httpx

from .data_models import EstateType, Locality, Estate, Company, Gps, Estate

import re

RE_ADDRESSES = [
    re.compile(r"(?P<street>[\D \d]+), (?P<city>\D+)"),
    re.compile(r"(?P<city>\D+) - (?P<district>\D+)"),
    re.compile(r"(?P<city>\D+) - (?P<district>\D+), (?P<region>\D+)"),
    re.compile(r"(?P<street>[\D \d]+), (?P<city>\D+) - (?P<district>\D+)"),
]


class InvalidEstate(Exception):
    pass


def normilize(text: str) -> str:
    return unicodedata.normalize("NFKD", text)


def parse_name(name: str) -> Tuple[EstateType, int]:
    # Prodej bytu 3+kk 123 m²
    replaces = [
        "Dražba bytu ",
        "Prodej bytu ",
        " m²",
        " m2",
        " (Mezonet)",
        " (Podkrovní)",
        " (Loft)",
    ]

    name = normilize(name)

    for r in replaces:
        name = name.replace(r, "")

    et_type, size = name.split()

    return EstateType(et_type), int(size)


def parse_locality(locality: str) -> Optional[Locality]:
    # Plzeň - Jižní Předměstí, okres Plzeň-město
    # Merhautova, Brno - Černá Pole
    result_locality = None

    for re_address in RE_ADDRESSES:
        match = re_address.match(locality)

        if match:
            result_locality = Locality(**match.groupdict())

    return result_locality


async def parse_one(r: Dict) -> Estate:
    # parse company
    company = None

    if "company" in r["_embedded"]:
        company_json = r["_embedded"]["company"]

        company = Company(
            id=company_json["id"],
            ico=company_json.get("ico"),
            name=company_json["name"],
        )

    gps = None
    if "gps" in r:
        gps = Gps(
            lat=r["gps"]["lat"],
            lon=r["gps"]["lon"],
        )

    # parse estate
    et_type, size = parse_name(
        r["name"],
    )

    estate = Estate(
        hash_id=r["hash_id"],
        size=size,
        locality=parse_locality(r["locality"]),
        et_type=et_type,
        price=r["price"],
        gps=gps,
        company=company,
    )

    return estate


async def parse(r_json: Dict) -> List[Estate]:
    estates = await asyncio.gather(
        *[parse_one(r) for r in r_json["_embedded"]["estates"]],
        return_exceptions=True,
    )

    return estates


async def paginate(params: Dict, per_page: int = 20) -> Tuple[List[Dict], int]:
    # get total number
    async with httpx.AsyncClient() as client:
        resp_json = await make_request(client, params, page=1, per_page=per_page)
        total_number = resp_json["result_size"]

    # pagenate results
    # page_range = range(2)
    page_range = range(math.ceil(total_number / per_page))

    async with httpx.AsyncClient() as client:
        respondes_json = await asyncio.gather(
            *[make_request(client, params, page, per_page) for page in page_range]
        )

    return respondes_json


async def make_request(
    client: httpx.AsyncClient,
    params: dict,
    page: int,
    per_page: int,
):
    base_url = "https://www.sreality.cz/api/cs/v2/estates"

    # replace per_page and page before making request
    params.update(
        {
            "page": page,
            "per_page": per_page,
        }
    )

    resp = await client.get(base_url, params=params)

    return resp.json()
