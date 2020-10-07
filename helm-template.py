import yaml
from pathlib import Path
import sys
from tempfile import TemporaryDirectory, NamedTemporaryFile
import subprocess
import shutil


# will be placed on /tmp
config_file = Path(sys.argv[1])

with config_file.open() as f:
    config = yaml.safe_load(f)


base_dir = None
tmpdir = None
tmp_values = None

caching_wanted = config['localCache']
cache_dir = Path('.') / "helm" / f"{config['chart']['name']}-{config['chart']['version']}"
base_dir = cache_dir

if not cache_dir.exists() or not caching_wanted:

    tmpdir = TemporaryDirectory()
    tmpdirpath = Path(tmpdir.name)

    cmd = f"""
        helm pull 
        --repo={config['chart']['repository']}
        --destination={tmpdirpath / "helm"}
        --untar 
        --version={config['chart']['version']}
            {config['chart']['name']}
    """

    rendered_manifests = subprocess.check_output(
        cmd.split(), encoding="utf-8"
    )

    if caching_wanted:
        shutil.move(tmpdirpath / "helm" / config['chart']['name'], cache_dir)
    else:
        base_dir = tmpdirpath  
            

cmd = f"""
    helm template 
    --name-template {config['metadata']['name']}
    {base_dir}
"""


# FIXME use `valuesFiles` with an array instead
if "valueFile" in config:
    for valueFile in config['valueFiles']:
        cmd += f" --values={valuesFile}"

if "values" in config:
    tmp_values = NamedTemporaryFile()
    yaml.safe_dump(config['values'], tmp_values, encoding='utf-8')

    cmd += f" --values={Path(tmp_values.name)}"

if "namespace" in config["metadata"]:
    cmd += f" --namespace={config['metadata']['namespace']}"

# --validate                     validate your manifests against the Kubernetes cluster you are currently pointing at. This is the same validation performed on an install
# --no-hooks ?
# --include-crds
# --skip-crds

rendered_manifests = subprocess.check_output(
    cmd.split(), 
    encoding="utf-8"
)

if tmp_values:
    tmp_values.close()

if tmpdir:
    tmpdir.cleanup()

print(rendered_manifests)
