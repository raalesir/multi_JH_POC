from flask import Flask
from flask import render_template
from flask import request
import glob
import re
import subprocess
import random

#TODO introduce LOGGING.... :)

CLUSTER = [
    '192.168.1.10',
    '192.168.1.11'
]

USERS = ['ubuntu', 'juser1']

#template for the *running* Jupyter server file
Jupyter_server_file = '/home/xxx/.local/share/jupyter/runtime/nbserver*.json'

app = Flask(__name__)


@app.route('/', methods=['POST', "GET"])
def index():
    name = None
    error = None
    msg = None
    links = None
    PID=[]
    ips=[]
    if request.method == "POST":
        name = request.form['username']
        if name  in  USERS:
            running_jupyter_servers = get_jupyter_servers(name)
            print(running_jupyter_servers)
            if len(running_jupyter_servers) > 1:
                msg="It looks like you are running multiple servers!!!!<br/> Please run just one" \
                     "server at a time. Returning the first in the list.<br/>"
            elif len(running_jupyter_servers) == 1:
                msg="This is the link to your running Jupyter server. <br/>Please\
                        remember to shutdown notebooks and Jupyter server when not in use...<br/>\
                                After session LOGOUT if want to keep your data private"
            else:
                msg = "It looks like you have no running Jupyter servers. Just follow the link"
                ips.append(get_new_ip()) # .append(random.choice(CLUSTER))

            for server in running_jupyter_servers:
                ips.append(get_ip(server))

            print(ips)
            return render_template("jh_seb.html", name=name, error=error,
                                   links=ips, msg=msg)
        else:
            error = "System does not recognize you. <br/> Please check username."
            name = None
    # print "get method "#,request.form['username']
    return render_template("jh_seb.html", name=name, error=error)



def get_ip(server):
    """
    Extracts the PID from the string ``server`` and finds IP of the PID

    :param server: the string like `/home/ubuntu/.local/share/jupyter/runtime/nbserver-2085.json`
    :return: the `IP` running the ``Jupyter`` server with the given `PID`
    """
    pid = re.findall(r"\d+", server)[-1]
    #print server, pid
    ip = find_host(pid)

    return ip



def find_host(pid):
    """
    Find a host based on the ``PID`` of the ``Jupyter`` server

    :param pid: the ``PID`` of the server
    :return: ``None`` if not found, hostname otherwise
    """
    # ssh to each node and get IP of the node with running  on
    #  user's behalf Jupyterhub
    result = None
    for host in CLUSTER:
        print(host, pid)
        result = check_host(host, pid)
        if result:
            return host



def get_new_ip():
    """
    function selects one of the nodes in the `CLUSTER` based on some
    rule...\n
    At the moment it is just a random choice between available hosts:
    ``[random.choice(CLUSTER)][0]``

    :return: ``IP`` address of the selected node
    """
    return [random.choice(CLUSTER)][0]



def get_jupyter_servers(username):
    """
    Are there Jupyter servers running and how many for the ``username``?

    :param username: username at SEB cluster
    :return:    list of running `Jupyter` servers
    """
    servers =[]
    servers = Jupyter_server_file.replace('xxx', username)
    servers = glob.glob(servers)

    return servers



def check_host(host, pid):
    """
    Log in to the HOST and check if the PID is running there.

    :param host: hostname
    :param pid:  PID to search
    :return: True if found, False otherwise
    """
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND = "ps -p " + pid + "|grep 'jupyterhub'"
    print(host, COMMAND)

    result, error = execute_remote_command_ssh(host, COMMAND) # ssh.stdout.readlines()
    if result == []:
        #error = ssh.stderr.readlines()
        print("ERROR: %s" % error)
        return False
    else:
        return True


def execute_remote_command_ssh(host, command):
    """
    executes a command on the remote host using `ssh`.
    Assumes passwordless inter-host connection.

    :param host: host to connect to
    :param command: Command to execute
    :return: tuple of the command output and error message
    """
    error=None
    ssh = subprocess.Popen(["ssh", "%s" % host, command],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
    return result, error


if __name__ == '__main__':
    app.run()
