# egi-fedcloud-im-tosca

Example files to use [Infrastructure Manager client](https://imdocs.readthedocs.io/en/latest/client.html)
on the [EGI Federated Cloud](https://www.egi.eu/services/cloud-compute/).

Note: The code here is intended to be used within the
[EGI Notebooks service](https://www.egi.eu/services/notebooks/).

# Configuration

Use conda to setup a dedicated Python environment the first time you use this repository:

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
source conda_deactivate.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh
conda install mamba -c conda-forge --yes
mamba create -n im-client python --yes
conda activate im-client
pip install IM-client
````

## Activate the conda environment

Subsequent use of the repository only needs activating the conda environment as follows:

```bash
source conda_deactivate.sh
source conda-install/etc/profile.d/conda.sh
conda activate im-client
```

## conda_deactivate.sh

Here is the `conda_deactivate.sh` script mentioned above:

```bash
#!/usr/bin/env bash

# copied from https://github.com/AMIGA-IAA/hcg-16/blob/master/run.sh

  EXISTS_CONDA=$(which conda) || $(echo "")

  if [[ "${EXISTS_CONDA}" ]] ; then
    CONDA_PATH=$(dirname $(dirname ${EXISTS_CONDA}))
    PATH_LIST=$(echo ${PATH} | tr ':' ' ')
    NEW_PATH=/usr/local/bin

    # loop to get rid of conda paths in PATH
    for e in $(echo ${PATH_LIST});
    do
      if [[ "${e}" != ${CONDA_PATH}* ]] && [[ "${e}" != "/usr/local/bin" ]] ; then
        NEW_PATH=${NEW_PATH}:${e}
      fi
    done

    # reconfig PATH
    PATH=${NEW_PATH}

    # loop to unset CONDA environment variables
    for e in $(env | grep CONDA | sed 's/=.*//g');
    do
      unset ${e}
    done

  fi
```

We use this script to avoid interfering with the available `conda` installation on the Notebooks.

# Workflow

Use the script `generate-im-client-files.py` to generate configuration files for `im-client.py`.

```bash
python generate-im-client-files.py --vo training.egi.eu --site IFCA-LCG2
python generate-im-client-files.py --vo training.egi.eu --site CESNET-MCC
python generate-im-client-files.py --vo training.egi.eu --site NCG-INGRID-PT
python generate-im-client-files.py --vo training.egi.eu --site IISAS-FedCloud
```

`generate-im-client-files.py` takes two template files as input that should located
on the same working directory:
* `vo-site-auth.dat`: template file to access a site with a VO
* `vo-site-tosca.yaml`: template file to deploy a single VM using TOSCA

The script replaces the text `SITE` and `VO` in both template files with the values
supplied as arguments (i.e. `--site` and `--vo`). Two new files are generated that
are ready to be used with `im-client.py`. See examples below.

In order to be organized, it is good to create a folder per VO and move all config files under it:

```bash
mkdir training.egi.eu
mv training.egi.eu-* training.egi.eu/
```

Once the auth and TOSCA files are properly generated, use `im-client.py` as follows:

```bash
im_client.py -a training.egi.eu-IFCA-LCG2-auth.dat create training.egi.eu-IFCA-LCG2-tosca.yaml
im_client.py -a training.egi.eu-CESNET-MCC-auth.dat create training.egi.eu-CESNET-MCC-tosca.yaml
im_client.py -a training.egi.eu-NCG-INGRID-PT-auth.dat create training.egi.eu-NCG-INGRID-PT-tosca.yaml
im_client.py -a training.egi.eu-IISAS-FedCloud-auth.dat create training.egi.eu-IISAS-FedCloud-tosca.yaml
```

For these commands to work properly we need the `im_client.cfg` file on the same working directory.

Other useful commands:

```bash
im_client.py list # it's much better to check https://appsgrycap.i3m.upv.es:31443/im-dashboard/infrastructures instead
im_client.py create tosca.yaml
im_client.py getstate <infra-id>
im_client.py ssh <infra-id>
im_client.py sshvm <infra-id> <vm-id>
im_client.py destroy <infra-id>
```

# TOSCA examples

Here we gather locations with example TOSCA files:
* https://github.com/grycap/im/tree/master/examples
* https://github.com/grycap/im-client/blob/master/test/files/tosca.yml
* https://github.com/indigo-dc/tosca-types/tree/master/examples
