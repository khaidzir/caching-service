import asyncio
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PayloadCache, TransformerCache
from .utils import hash, interleave_strings, transformer_function


class DifferentInputLengthError(Exception):
    pass


async def create_payload(
    list_1: list[str], list_2: list[str], session: AsyncSession
) -> uuid.UUID:
    if len(list_1) != len(list_2):
        raise DifferentInputLengthError("The two lists must have the same length")

    # Order the lists to ensure the same hash value for the same input.
    input_lists = [list_1, list_2]

    # Use json.dumps to convert the lists to a JSON string.
    hashed_payload = hash(json.dumps(input_lists))

    payload_cache = await session.execute(
        select(PayloadCache).filter(PayloadCache.hash == hashed_payload)
    )
    payload_cache = payload_cache.scalar_one_or_none()

    if payload_cache:
        return payload_cache.id

    # Check if the transformer function is already in the database.
    hashed_inputs_1 = []
    hashed_inputs_2 = []
    for str1 in list_1:
        hashed_inputs_1.append(hash(str1))
    for str2 in list_2:
        hashed_inputs_2.append(hash(str2))

    # Check if the transformer function output for each individual input
    # is already in the database.
    # Query all transformer caches in a single database call.
    # Create a mapping of existing transformer caches by their hash
    transformer_caches = await session.execute(
        select(TransformerCache).filter(
            TransformerCache.hash.in_(hashed_inputs_1 + hashed_inputs_2)
        )
    )
    existing_caches = {tc.hash: tc for tc in transformer_caches.scalars().all()}

    # Create new transformer caches for missing entries
    to_transforms: list[tuple[str, str]] = []
    for input_hash, str1 in zip(hashed_inputs_1, list_1):
        if input_hash not in existing_caches:
            to_transforms.append((input_hash, str1))
    for input_hash, str2 in zip(hashed_inputs_2, list_2):
        if input_hash not in existing_caches:
            to_transforms.append((input_hash, str2))

    # Call the transformer function for the missing entries
    transformed_outputs = await asyncio.gather(
        *[transformer_function(str_) for _, str_ in to_transforms]
    )

    # Create a mapping of new transformer caches by their hash
    new_caches = {
        to_transform[0]: transformed_output
        for to_transform, transformed_output in zip(to_transforms, transformed_outputs)
    }

    # Create new transformer caches for the missing entries
    for to_transform, transformed in zip(to_transforms, transformed_outputs):
        session.add(
            TransformerCache(
                hash=to_transform[0], string_input=to_transform[1], result=transformed
            )
        )

    # Create the payload result
    transformed_list_1 = []
    for input_hash in hashed_inputs_1:
        if input_hash in existing_caches:
            transformed_list_1.append(existing_caches[input_hash].result)
        else:
            transformed_list_1.append(new_caches[input_hash])

    transformed_list_2 = []
    for input_hash in hashed_inputs_2:
        if input_hash in existing_caches:
            transformed_list_2.append(existing_caches[input_hash].result)
        else:
            transformed_list_2.append(new_caches[input_hash])

    result = interleave_strings(transformed_list_1, transformed_list_2)

    # Add PayloadCache to the database
    result_id = uuid.uuid4()
    payload_cache = PayloadCache(
        id=result_id,
        hash=hashed_payload,
        input_payload=input_lists,
        output=result,
    )
    session.add(payload_cache)

    await session.commit()

    return result_id


async def get_payload(id: uuid.UUID, session: AsyncSession) -> PayloadCache | None:
    payload_cache = await session.execute(
        select(PayloadCache).filter(PayloadCache.id == id)
    )
    return payload_cache.scalar_one_or_none()
