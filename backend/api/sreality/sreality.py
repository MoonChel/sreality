import asyncio
from urllib.parse import urlparse, parse_qsl

from .data_models import Result
from .utils import paginate, parse
from .url_parser import url_parser


async def sreality(url: str) -> Result:
    params = url_parser(url)

    resps_json = await paginate(params, per_page=20)

    result = Result(
        estates=[],
        result_size=0,
        title=resps_json[0]["meta_description"].split(".")[0] + ".",
        total_number=resps_json[0]["result_size"],
    )

    estates = await asyncio.gather(
        *[parse(rj) for rj in resps_json],
        return_exceptions=True,
    )

    for es in estates:
        # filter out exceptions
        es = [e for e in es if not isinstance(e, Exception)]

        result.estates += es

    result.result_size = len(result.estates)

    # additional params for charts
    result.min_price = min(result.estates, key=lambda x: x.price).price
    result.max_price = max(result.estates, key=lambda x: x.price).price
    result.min_size = min(result.estates, key=lambda x: x.size).size
    result.max_size = max(result.estates, key=lambda x: x.size).size

    return result
