import enum
from typing import Optional, List
from dataclasses import dataclass


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
    total_number: int
    estates: List[Estate]
