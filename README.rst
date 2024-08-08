=========
nada-data
=========

Python library to enable tabular data operations with `nada-dsl <https://pypi.org/project/nada-dsl/>`__.

Purpose
-------


Installation and Usage
----------------------

This library is available as a `package on PyPI <https://pypi.org/project/nada-data>`__:

.. code-block:: bash

    python -m pip install nada-data


The library can be imported in the usual way:

.. code-block:: python

    import nada_data
    from nada_data import *


The library provides two basic types: ``NadaArray`` and ``NadaTable``. The **NadaArray** type is analogous
to Python's builtin ``list`` type, and can be created as follows:

.. code-block:: python

    from nada_dsl import SecretInteger, Input, Party
    from nada_data import NadaArray

    party = Party(name="me")

    # can be instantiated as comma-separated list of values
    arr = NadaArray(
        SecretInteger(Input(name="int1", party=party)),
        SecretInteger(Input(name="int2", party=party))
    )

    # OR from list
    values = [SecretInteger(Input(name="int1", party=party)), SecretInteger(Input(name="int2", party=party))]
    arr = NadaArray(values)

    # OR as list comp from list
    arr = NadaArray(v for v in values)

    >>> arr
    NadaArray | len=2 | parties=['me']


For ``NadaArray``, utility functions that are normally available to the ``list`` type:

.. code-block:: python

    from nada_data import sum_nada_array, filter_nada_array, nada_gt

    # sum a NadaArray, outputting a single SecretInteger
    s = sum_nada_array(arr)

    new_party = Party(name="new_party")
    # filter a NadaArray according to which values are greater than 'int3'
    f = filter_nada_array(arr, nada_gt, SecretInteger(Input(name="int3", party=new_party)))

    # display metadata about this NadaArray
    >>> f
    NadaArray | len=2 | parties=['me', 'new_party']


The ``NadaTable`` type is a tabular data structure that enables relational workflows over arrays of ``SecretInteger``
instances. Accordingly, it is instantiated from an array of ``NadaArray`` objects and a comma-separated list of
column names:


.. code-block:: python

    from nada_data import NadaTable

    rows = [
        NadaArray(SecretInteger(Input(name="int1", party=party)), SecretInteger(Input(name="int2", party=party))),
        NadaArray(SecretInteger(Input(name="int3", party=new_party)), SecretInteger(Input(name="int4", party=new_party)))
    ]

    tbl = NadaTable(
        "a", "b", rows=rows
    )
    >>> tbl
    NadaTable | cols=['a','b'] | rows=2 | parties=['me','new_party']


The **NadaTable** type provides relational-style functions that one would expect from something like a SQl table:

.. code-block:: python

    # select one or more columns into a new table
    col = tbl.select("a")
    >>> col
    NadaTable | cols=['a'] | rows=2 | parties=['me', 'new_party']

    # sum column 'b' ordered over column 'a'
    tbl.aggregate_sum(key_col="a", agg_col="b")
    >>> tbl
    NadaTable | cols=['a','b'] | rows=2 | parties=['me','new_party']


Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The
``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__
for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and
so on) when performing installation using `pip <https://pypi.org/project/pip>`__:

.. code-block:: bash

    python -m pip install .[docs,lint]


Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__:

.. code-block:: bash

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html


Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^

All unit tests are executed using a combination of `doctest` and `unittest`. Both can be run simultaneously via
the following:

.. code-block:: bash

    python -m pip install .[test]
    python -m unittest discover -s tests


Coverage can be measured while the tests are run using `coverage`:

.. code-block:: bash

    coverage run -m unittest discover -s tests
    coverage report


Style conventions are enforced using `Pylint <https://pylint.readthedocs.io>`__:

.. code-block:: bash

    python -m pip install .[lint]
    python -m pylint src/nada_data


Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the
`GitHub page <https://github.com/choosek/nada-data>`__ for this library.


Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments
conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.


Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/nada-data>`__ by a package maintainer.
First, install the dependencies required for packaging and publishing:

.. code-block:: bash

    python -m pip install .[publish]


Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to
the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure
that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__
that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing
``?.?.?`` with the version number):

.. code-block:: bash

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive:

.. code-block:: bash

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__:

.. code-block:: bash

    python -m twine upload dist/*
