import aiohttp
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, model_validator


class Sidejob(BaseModel):
    id: int
    label: str
    job_title_extra: Optional[str] = None
    api_url: str
    category: str
    organization_label: Optional[str] = None
    organization_country: Optional[str] = None
    income_total: Optional[float] = None

    @model_validator(mode='before')
    @classmethod
    def flatten(cls, data: Any) -> Any:
        org = data.get("sidejob_organization")
        if isinstance(org, dict):
            data["organization_label"] = org.get("label")
            country = data.get("field_country")
            if isinstance(country, dict):
                data["organization_country"] = country.get("label")
        if data.get("income_total") is None:
            data["income_total"] = 0.0
        return data

async def load_sidejobs(
        politician_mandate_id: int,
        session: aiohttp.ClientSession,
) -> List[Sidejob]:
    """
    Calls the abgeordnetenwatch API to retrieve all sidejobs for a given politician mandate.

    :param politician_mandate_id: mandate id for politician
    :param session: aiohttp session to use for making the request.
    :return: The sidejob with the given id.
    """
    params = {'mandates': politician_mandate_id}
    url = 'https://www.abgeordnetenwatch.de/api/v2/sidejobs'
    async with session.get(url, raise_for_status=True, params=params) as r:
        data = await r.json()
        return [Sidejob.model_validate(job_data) for job_data in data['data']]