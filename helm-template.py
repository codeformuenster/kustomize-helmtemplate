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

cmd = f"""
    helm template 
    {config['chartName']}
    {base_dir}
    --values={config['valuesFile']}
"""

rendered_manifests = subprocess.check_output(
    cmd.split(), 
    encoding="utf-8"
)

if tmpdir:
    tmpdir.cleanup()

print(rendered_manifests)
