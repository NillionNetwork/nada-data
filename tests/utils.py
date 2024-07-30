from typing import List
from nada_dsl import audit
from nada_data import NadaArray


def serialize_input_array(arr: List[int], party: audit.Party, prefix: str) -> NadaArray:
    return NadaArray(
        audit.SecretInteger(
            audit.Input(f"{prefix}{i}", party=party)
        ) for i in range(len(arr))
    )


def initialize_table_data(arrs: List[List[int]]):
    audit.Abstract.initialize(
        {f"p1_input_{i}_{j}": val for i, row in enumerate(arrs) for j, val in enumerate(row)}
    )


def serialize_input_table(arrs: List[List[int]], party: audit.Party, prefix: str) -> List[NadaArray]:
    return [
        NadaArray(
            audit.SecretInteger(
                audit.Input(f"{prefix}{i}_{j}", party=party)
            ) for j in range(len(arrs[i]))
        ) for i in range(len(arrs))
    ]
