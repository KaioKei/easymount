# EasyMount

Mount VMs by configuration using VirtualBox, Vagrant and Jinja2

## Requirements

Environment :

| **Package** | **Version** |
| --- | --- |
| Python | \>= 3.8.5 |
| Pip | \>= 21.0.1 |
| VirtualBox | \>= 6.1.18 |

Python modules :

```sh
pip install -r requirements.txt
```

## Install

```sh
# install easymount environment
./install.sh
easymount -h
```

## Getting started

Mount two CentOS 8 VMs:

```sh
easymount mount -c simple_conf_example.yaml
```

Only configure a Vagrant file and save it to `/tmp`:

```sh
easymount configure -c simple_conf_example.yaml -o /tmp
```

## Configuration

The configuration is provided as a Yaml file. This project contains 2 examples :

* [A simple and quick configuration](./simple_conf_example.yaml)
* [A more detailed configuration](./detailed_conf_example.yaml)

The configuration is platform-based :

| **Configuration** | **Mandatory** | **Default Value** | **Description** |
| --- | --- | --- | --- |
| platform.box | Yes, or override per server | None | The Vagrant box to install on all servers. |
| platform.user | No | `vagrant`| The sudoer user to install on all servers. The public ssh key of your host will be authorized for this host. |
| platform.memory | No | `4096` | The amount of RAM to install on all servers. |
| platform.vcpu | No | `1` | The amount of vCPUs to install on all servers. |
| platform.ssh_pubkey | No | `~/.ssh/id_rsa.pub` | The path of the ssh public key of your host to install as the authorized key for `user` on all the servers. |
| platform.selinux | No | `true` | If `false`, disable Selinux on all servers. If `true`, change nothing. Keep `true` on a debian based OS. |

Each platform's server MUST be configured :

| **Configuration** | **Mandatory** | **Default Value** | **Description** |
| --- | --- | --- | --- |
| platform.hostname | Yes | None | The current server name. This name will be used for DNS resolution on the other severs. |
| platform.ip | No | `192.168.50.1x`, `x` being the server index order in the current list. | The host IP of the current server.|
| platform.box | No | `platform.box` | Overrides the Vagrant box to install on the current server. |
| platform.memory | No | `platform.memory` | Overrides the amount of RAM to install on the current servers. |
| platform.vcpu | No | `platform.vcpu` | Overrides the amount of vCPUs to install on the current servers. |
| platform.selinux | No | `platform.selinux` | Overrides the selinux option on the current server. |