from typing import Dict, List

from logic.apps.cards import repository
from logic.apps.cards.error import CardError
from logic.apps.cards.model import Card
from logic.apps.jobs import service as job_service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger


def exec(card: Card) -> str:

    job = card.to_job()
    job_service.add(job)

    logger.log.info(f'Card {card.name} -> Making new job with id {job.id}')

    return job.id


def add(card_work: Card) -> str:

    if repository.get(card_work.id):
        raise AppException(CardError.CARD_ALREDY_EXIST_ERROR,
                           f'There are a card with id {id}')

    repository.add(card_work)
    return card_work.id


def get(id: str) -> Card:
    return repository.get(id)


def get_all(filter: str = None) -> List[Card]:
    return repository.get_all(filter)


def delete(id: str):
    if not repository.exist(id):
        raise AppException(CardError.CARD_NOT_EXIST_ERROR,
                           f'There are no card with id {id}')

    repository.delete(id)


def list_all() -> List[str]:
    return [
        card.id
        for card
        in repository.get_all()
    ]


def get_all_short(filter: str = None) -> List[Dict[str, str]]:
    return [
        {
            "name": c.name,
            "description": c.description,
            "color": c.color,
            "job_agent_type": c.job_agent_type,
            "job_module_name": c.job_module_name,
            "job_module_repo": c.job_module_repo,
            "creation_date": c.creation_date.isoformat(),
            "id": c.id
        }
        for c in repository.get_all(filter)
    ]


def modify(card: Card):
    repository.delete(card.id)
    repository.add(card)


def run(id: str, params: Dict[str, object]) -> str:

    card = get(id)
    if not card:
        raise AppException(CardError.CARD_NOT_EXIST_ERROR,
                           f'There are no card with id {id}')

    return job_service.add(card.to_job(params))


def post_docs(id: str, docs: str):

    card = get(id)
    if not card:
        raise AppException(CardError.CARD_NOT_EXIST_ERROR,
                           f'There are no card with id {id}')

    card.job_default_docs = docs
    modify(card)


def get_docs(id: str):

    card = get(id)
    if not card:
        raise AppException(CardError.CARD_NOT_EXIST_ERROR,
                           f'There are no card with id {id}')

    return card.job_default_docs
