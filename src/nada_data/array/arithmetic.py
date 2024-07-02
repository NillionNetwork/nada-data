from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.array.nada_array import NadaArray


secret_int_types = {SecretInteger, audit.abstract.SecretInteger}
secret_int = Union[*secret_int_types]


def sum_nada_array(argument: Union[List[secret_int], NadaArray]) -> secret_int:
    """
    Sum an array of SecretInteger objects
    """

    output = argument[0]
    for e in argument[1:]:
        if type(e) not in secret_int_types:
            raise TypeError(f"all input values must be of type SecretInteger")
        output = output + e

    return output
