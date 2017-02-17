Problem in focus:
-----------------
The purpose of the module is to provide a simple way to orchestrate multiple
[JupyterHub](https://jupyterhub.readthedocs.io/en/latest/) servers over a set
of hosts.

One JupyterHub server allows to run multiple single-user [Jupyter]
(http://jupyter.org) servers.
One of the bottlenecks of running many Jupyter servers on a single host -- lack
of memory.

The challenge:
--------------
One of the ways to go is to
launch multiple JupyterHub servers, each running on a  **different** node. In
this case the memory pressure is decreased.
The challenge is to be able to track the node on which the user runs his
single-user `Jupyter` server, so his can
continue to work with the notebook after logging out from the JupyterHub UI.

