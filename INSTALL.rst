Building a Python ZIP Application
---------------------------------

To create a self-contained package including dependencies and binaries for you
system from the sources install shiv_.

Download the source tarball from the Releases_ page, extract its contents,
change into its root directory and run:

.. code-block:: console

    $ shiv -o quick-csr-<OS identifier>-<CPU architecture>.pyz -c quick-csr .

Installation as Python package
------------------------------

Beside obtaining ``quick-csr`` as ZIP Application, it can be installed the
'classic' way.

This is not recommended for users that are unexperienced with Python packaging
and don't want to poke into its historical legacy.
There's currently no package published on the Python Package Index, therefore
you have to obtain the source code, change into its root directory and run:

.. code-block:: console

    $ pip install --user .

Finally, to install a hackable instance of the software (assuming you created
a virtual environment):

.. code-block:: console

    $ pip install --user --editable .

.. _releases: https://github.com/telota/quick-csr/releases
.. _shiv: https://github.com/linkedin/shiv
