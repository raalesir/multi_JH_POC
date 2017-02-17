.. multiJHub documentation master file, created by
   sphinx-quickstart on Thu Feb 16 21:56:43 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Brief multiJHub's POC
=====================

Problem in focus:
-----------------
The purpose of the module is to provide a simple way to orchestrate multiple
`JupyterHub <https://jupyterhub.readthedocs.io/en/latest/>`_ servers over a set of hosts.

One JupyterHub server allows to run multiple single-user `Jupyter <http://jupyter.org>`_ servers.
One of the bottlenecks of running many Jupyter servers on a single host -- lack of memory.

The challenge:
--------------
One of the ways to go is to
launch multiple JupyterHub servers, each running on a  **different** node. In this case the memory pressure is decreased.
The challenge is to be able to track the node on which the user runs his single-user `Jupyter` server, so his can
continue to work with the notebook after logging out from the JupyterHub UI.

Alternatives:
-------------
There are several ready to use `solutions <https://github.com/jupyterhub/jupyterhub/wiki/Spawners>`_,
which probably are more scalable, but require more **intrusion**
into the already existing infrastructure, what can be pretty undesirable.

Proposed solution:
------------------
A simple, though not complete, solution is proposed to tackle this challenge, introducing  minimal changes to the
existing infrastructure.
The solution uses ``Flask`` webserver and works under the following assumptions:

1. the hosts must have **passwordless** ``ssh`` connection to each other
2. it should be certain flexibility to open ports above 8000
3. it should be possible to install ``NFS`` into the nodes

One of the hosts shares with ``NFS`` the ``$HOME`` where the all ``Jupyter`` users have their accounts,
i.e. `/home/juser1`, `/home/juser2`.
The ``$HOME`` is being exported to the rest nodes subjected to run ``JupyterHub`` servers, one server per node.

The user, who runs the ``Flask`` webserver, is able to read recursively the ``$HOME`` for each ``JupyterHub`` user.
It is needed in order to be able to figure out the connection between the user and the ``Jupyter`` server he/she runs.
This is achieved with the Access Control Lists (ACLs).
For example, in order to allow group ``flask_users`` to have read access to the
``/home/juser1/.local/share/jupyter/runtime/`` directory, storing the data about running ``Jupyter`` servers and
notebooks, one has to issue:
``sudo setfacl -md g:flask_users:r /home/juser1/.local/share/jupyter/runtime/``.
This setup while allowing for the defined usergroup collect information about running ``Jupyter`` servers, still keeps
**isolation** between the ``Jupyter`` users.



Code docstrings:
----------------




.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. automodule:: JH_SEB
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
