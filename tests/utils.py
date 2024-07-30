from typing import List, Dict
from nada_dsl import audit
from nada_data import NadaArray


def serialize_input_array(arr: List[int], party: audit.Party, prefix: str) -> NadaArray:
    return NadaArray(
        audit.SecretInteger(
            audit.Input(f"{prefix}{i}", party=party)
        ) for i in range(len(arr))
    )


def serialize_input_table(arrs: List[List[int]], party: audit.Party, prefix: str) -> List[NadaArray]:
    return [
        NadaArray(
            audit.SecretInteger(
                audit.Input(f"{prefix}{i}_{j}", party=party)
            ) for j in range(len(arrs[i]))
        ) for i in range(len(arrs))
    ]


def initialize_array_data(prefix: str, arr: List[int]):
    audit.Abstract.initialize(
        {f"{prefix}{i}": arr[i] for i in range(len(arr))}
    )


def initialize_array_data_multi(inputs: Dict[str, List[int]]):
    audit.Abstract.initialize({
        f"{party_name}_{i}": inputs[party_name][i]
        for party_name in inputs.keys()
        for i in range(len(inputs[party_name]))
    })


def initialize_table_data(prefix: str, arrs: List[List[int]]):
    audit.Abstract.initialize(
        {f"{prefix}{i}_{j}": val for i, row in enumerate(arrs) for j, val in enumerate(row)}
    )
