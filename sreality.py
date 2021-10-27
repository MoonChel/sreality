import math
import enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import json
import unicodedata

import requests


@dataclass
class Company:
    id: int
    ico: Optional[int]
    name: str


class EstateType(enum.Enum):
    et_5_5 = "5+1"
    et_4_1 = "4+1"
    et_3_1 = "3+1"
    et_2_1 = "2+1"
    et_1_1 = "1+1"
    et_5_kk = "5+kk"
    et_4_kk = "4+kk"
    et_3_kk = "3+kk"
    et_2_kk = "2+kk"
    et_1_kk = "1+kk"

    def __deepcopy__(self, memo):
        return self.value


@dataclass
class Gps:
    lat: float
    lon: float


@dataclass
class Locality:
    city: str
    district: str
    region: str


@dataclass
class Estate:
    hash_id: int
    size: int
    locality: Locality
    price: int
    et_type: EstateType
    gps: Gps
    company: Optional[Company]


@dataclass
class Result:
    result_size: int
    estates: List[Estate]


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
    ]

    name = normilize(name)

    for r in replaces:
        name = name.replace(r, "")

    et_type, size = name.split()

    return EstateType(et_type), int(size)


def parse_locality(locality: str) -> Optional[Locality]:
    # Plzeň - Jižní Předměstí, okres Plzeň-město
    if " - " in locality:
        city, district_region = locality.split(" - ")
        district, region = district_region.split(", ")
    else:
        city = ""
        district, region = locality.split(", ")

    return Locality(
        city=city,
        district=district,
        region=region,
    )


def parse(r_json: Dict) -> List[Estate]:
    estates = []

    for r in r_json["_embedded"]["estates"]:
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

        estates.append(estate)

    return estates


def make_request(page: int, per_page: int):
    base_url = "https://www.sreality.cz/api/cs/v2/estates"
    params = {
        "category_main_cb": "1",
        "category_sub_cb": "5%7C6%7C7%7C8",
        "category_type_cb": "1",
        "locality_district_id": "12",
        "locality_region_id": "2",
        "page": page,
        "per_page": "20",
        "tms": "1632290181845",
        "usable_area": "60%7C10000000000",
    }

    resp = requests.get(base_url, params=params)

    return resp


def get_total_number(resp_json: Dict):
    return resp_json["result_size"]


def paginate(per_page: int = 20) -> Tuple[List[Dict], int]:
    result = []

    resp_json = make_request(
        page=1,
        per_page=per_page,
    ).json()

    total_number = get_total_number(resp_json)

    for page in range(math.ceil(total_number / per_page)):
        resp = make_request(
            page=page,
            per_page=per_page,
        )
        resp_json = resp.json()

        result.append(resp_json)

    return result, total_number


def sreality():
    resp_json, total_number = paginate(per_page=20)

    result = Result(
        estates=[],
        result_size=total_number,
    )

    for rj in resp_json:
        estates = parse(rj)
        result.estates += estates

    result_dict = asdict(result)
    result_json = json.dumps(
        result_dict,
        indent=4,
        ensure_ascii=False,
    )

    with open("result.json", "w") as output:
        output.write(result_json)

    return result


if __name__ == "__main__":
    sreality()
