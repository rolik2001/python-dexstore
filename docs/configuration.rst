*************
Configuration
*************

The pydexstore library comes with its own local configuration database
that stores information like

* API node URL
* default account name
* the encrypted master password

and potentially more, **persistently**.

You can access those variables like a regular dictionary by using

.. code-block:: python

    from dexstore import DexStore
    dexstore = DexStore()
    print(dexstore.config.items())

Keys can be added and changed like they are for regular dictionaries.

.. code-block:: python

    dexstore.config["my-new-variable"] = "important-content"
    print(dexstore.config["my-new-variable"])
