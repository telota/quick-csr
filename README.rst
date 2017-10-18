quick-csr
=========

A command-line tool to quickly generate *Certificate Signing Requests* (CSR_),
targeted to DAUs and busy people. The major desktop operating systems are
supported.


Installation
------------

Python 3.5 or later is required to install and run the tool.
There's currently no package published on the Python Package Index, therefore
you have to obtain the source code, change into its root directory and run:

.. code-block:: console

    $ pip install --user .

To avoid conflicts within a system's ``site-package``'s namespace, it is
however recommended to install any end-user-software in a separate virtual
environment with pipsi_:

.. code-block:: console

    $ pipsi install .

Finally, to install a hackable instance of the software (assuming you created
a virtual environment):

.. code-block:: console

    $ pip install -e .


What it does
------------

The tool takes at least one distinguished name as argument, creates a CSR
according to the `PKCS #10`_ specs for it, creates a key pair to sign it and
saves both to disk (the CSR in the ``PEM`` format). The CSR is to be handled by
a Certificate Authority, the keys are later used to unlock the delivered
certificate chain, e.g. on a web server.

.. important::

    The keys are not secured with a password, so keep them in a safe location!
    Or add a password with ``openssl``.


Configuration
-------------

The tool is intended for environments where most information of a
certificates's subject are usually the same. Before using it, these have to be
defined in a config file, which is per default looked up as ``.quick-csr.cfg``
in your user directory:

.. code-block:: ini

    [default]

    organizationalUnitName = web department
    organizationName = Center For Universal Bauhaus Studies
    localityName = Tel Aviv
    stateOrProvinceName = Tel Aviv
    countryName = IL


Deviant values for other usage contexts can be declared in further sections:

.. code-block:: ini

    [laboratory]

    organizationalUnitName = laboratory


Usage
-----

Once this is set up, you can quickly generate CSRs. These examples relate to
the example configuration from the previous section:

For a single ``commonName``:

.. code-block:: console

    quick-csr www.cubs.org.il

Including some alternative names:

.. code-block:: console

    quick-csr www.cubs.org.il cubs.org.il web.cubs.org.il

Now, with another profile for another OU (``laboratory``):

.. code-block:: console

    quick-csr -c :laboratory living-concrete.cubs.org.il


Required options
----------------

These options must be present at least in the ``defaults`` section:

- ``organizationalUnitName``
- ``organizationName``
- ``localityName``
- ``stateOrProvinceName``
- ``countryName``


Optional options
----------------

- ``key_size``
   - length of the generated key in bits
   - default: ``4096``
- ``target_folder``
   - the resulting files are written there
   - defaults to the current working directory


.. _CSR: https://en.wikipedia.org/wiki/Certificate_Signing_Request
.. _pipsi: https://pypi.python.org/pypi/pipsi
.. _`PKCS #10`: https://tools.ietf.org/html/rfc2986
