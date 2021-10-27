import asyncio
from urllib.parse import urlparse, parse_qsl

from .data_models import Result
from .utils import paginate, parse


async def sreality(url: str) -> Result:
    parsed_url = urlparse(url)
    params = dict(parse_qsl(parsed_url.query))

    resp_json, total_number = await paginate(params, per_page=20)

    result = Result(
        estates=[],
        result_size=0,
        total_number=total_number,
    )

    estates = await asyncio.gather(
        *[parse(rj) for rj in resp_json],
        return_exceptions=True,
    )

    for es in estates:
        # filter out exceptions
        es = [e for e in es if not isinstance(e, Exception)]

        result.estates += es

    result.result_size = len(result.estates)

    return result
