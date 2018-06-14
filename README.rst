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
----------------

These options must be present at least in the ``defaults`` section:

- ``organizationalUnitName``
- ``organizationName``
- ``localityName``
- ``stateOrProvinceName``
- ``countryName``


Additional options
------------------

- ``key_size``
   - length of the generated key in bits
   - default: ``4096``
- ``target_folder``
   - the resulting files are written there
   - defaults to the current working directory


.. _CSR: https://en.wikipedia.org/wiki/Certificate_Signing_Request
.. _pipsi: https://pypi.python.org/pypi/pipsi
.. _`PKCS #10`: https://tools.ietf.org/html/rfc2986


Use quick-csr as ZIP Application
--------------------------------
With Python 3.5+ installed, quick-csr can be run on any system by executing a appropriate Python ZIP Application that includes all its dependencies and system specific binaries.
See `releases <https://github.com/telota/quick-csr/releases>`_ to find ready-to-launch zip applications. If your OS is not (yet) supported, please head over to the next section.

Usage is as described below but with your *filename* instead of *quick-csr*:

.. code-block:: console

    $ CSR-win7.pyz www.cubs.org.il
Note that you have to be in the correct directory in the above case.
Therefore is suggested to setup an `alias <https://docs.microsoft.com/en-us/windows/console/console-aliases>`_
for a day-to-day usage:

.. code-block:: console

    $ doskey CSR=C:\Users\Me\Projekte\quick-csr\quick-csr-master\CSR-win7.pyz $*
Regardless of your current working directory you can now run: 

.. code-block:: console

    $ CSR www.cubs.org.il


Building a Python ZIP Application 
---------------------------------

To create a self-contained package including dependencies and binaries for you system, install `shiv <https://github.com/linkedin/shiv>`_. 

Download this repository, change into its root directory and run:

.. code-block:: console

    $ shiv -o CSR-YOUR_OS.pyz -c quick-csr .
Installation
------------

There's currently no package published on the Python Package Index, therefore
you have to obtain the source code, change into its root directory and run:

.. code-block:: console

    $ pip install --user .

To avoid conflicts within a system's ``site-package``'s namespace, it is
however recommended to install any end-user-software in a separate virtual
environment with pipsi_:

.. code-block:: console

    $ pipsi install .

Alternatively, good experiences had been made by using pyenv-virtualenv to set up a Python 3.5.2 environment in the local quick-csr-folder. Then you can skip possible pipsi problems.

 .. code-block:: console

    $ pyenv local quickcsr

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


