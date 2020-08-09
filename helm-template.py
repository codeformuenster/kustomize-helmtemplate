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

caching_wanted = config['localCache']
cache_dir = Path('.') / "helm" / f"{config['chartName']}-{config['chartVersion']}"

if not cache_dir.exists() or not caching_wanted:

    tmpdir = TemporaryDirectory()
    tmpdirpath = Path(tmpdir.name)

    cmd = f"""
        helm pull 
        --repo={config['repo']}
        --destination={tmpdirpath / "helm"}
        --untar 
        --version={config['chartVersion']}
            {config['chartName']}
    """

    rendered_manifests = subprocess.check_output(
        cmd.split(), encoding="utf-8"
    )

    if caching_wanted:
        shutil.move(tmpdirpath / "helm" / config['chartName'], cache_dir)
        
            
if caching_wanted:
    base_dir = cache_dir
else:
    base_dir = tmpdirpath

if "values" in config:
    tmp_values = NamedTemporaryFile()
    yaml.safe_dump(config['values'], tmp_values, encoding='utf-8')
    # config['valuesFile'] = Path(tmp_values.name)

cmd = f"""
    helm template 
    {config['chartName']}
    {base_dir}
"""
# FIXME use `valuesFiles` with an array instead
if "valuesFile" in config:
    cmd += f" --values={config['valuesFile']}"
if "values" in config:
    cmd += f" --values={Path(tmp_values.name)}"

# --values valueFiles            Specify values in a YAML file (can specify multiple) (default [])
# --validate                     validate your manifests against the Kubernetes cluster you are currently pointing at. This is the same validation performed on an install

rendered_manifests = subprocess.check_output(
    cmd.split(), 
    encoding="utf-8"
)

if tmp_values:
    tmp_values.close()

if tmpdir:
    tmpdir.cleanup()

print(rendered_manifests)
