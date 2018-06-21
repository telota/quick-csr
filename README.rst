quick-csr
=========

A command-line tool to quickly generate *Certificate Signing Requests* (CSR_),
targeted to DAUs and busy people. The major desktop operating systems are
supported.

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

Required options
~~~~~~~~~~~~~~~~

These options must be present at least in the ``defaults`` section:

- ``organizationalUnitName``
- ``organizationName``
- ``localityName``
- ``stateOrProvinceName``
- ``countryName``

Additional options
~~~~~~~~~~~~~~~~~~

- ``key_size``
   - length of the generated key in bits
   - default: ``4096``
- ``target_folder``
   - the resulting files are written there
   - defaults to the current working directory

Use quick-csr as Python ZIP Application
---------------------------------------

With Python 3.5+ installed, ``quick-csr`` can be run on any system by executing
an appropriate Python ZIP Application that includes all its dependencies and
system specific binaries.
See the Releases_ page to find ready-to-launch zip applications. If your OS is
not (yet) supported, please head over to INSTALL.rst_ or open an issue_ to
request one.

Usage is as described below but with the system specific *filename* instead of
``quick-csr``:

.. code-block:: console

    $ quick-csr-win10.pyz www.cubs.org.il

Note that the current working directory has to be in the directory in this
case.

Therefore it is suggested to setup an alias for a day-to-day usage.

On POSIX compliant systems in an appropriate file, e.g. ``~/.bash_aliases``:

.. code-block:: console

    alias quick-csr='~/…/quick-csr-linux-amd64.pyz'

On windows, use the doskey_ command to setup an alias:

.. code-block:: console

    $ doskey quick-csr=C:\\Users\\Me\\quick-csr-win10.pyz $*

Regardless of your current working directory you can now run:

.. code-block:: console

    $ quick-csr www.cubs.org.il


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


.. _doskey: https://docs.microsoft.com/en-us/windows/console/console-aliases
.. _CSR: https://en.wikipedia.org/wiki/Certificate_Signing_Request
.. _issue: https://github.com/telota/quick-csr/issues
.. _pipsi: https://pypi.python.org/pypi/pipsi
.. _`PKCS #10`: https://tools.ietf.org/html/rfc2986
.. _releases: https://github.com/telota/quick-csr/releases
.. _shiv: https://github.com/linkedin/shiv
.. _INSTALL.rst: /INSTALL.rst