from typing import List
from nada_dsl import audit
from nada_data import NadaArray


def serialize_input_array(arr: List[int], party: audit.Party, prefix: str) -> NadaArray:
    return NadaArray(
        audit.SecretInteger(
            audit.Input(f"{prefix}{i}", party=party)
        ) for i in range(len(arr))
    )


def serialize_input_table(arr: List[List[int]], party: audit.Party, prefix: str) -> List[NadaArray]:
    return [
        NadaArray(
            audit.SecretInteger(
                audit.Input(f"{prefix}{i}_{j}", party=party)
            ) for j in range(len(arr[i]))
        ) for i in range(len(arr))
    ]
