# kustomize plugin helm-template


```bash
mkdir -p "$HOME/.config/kustomize/plugin/helm-template.webwur.st/v1alpha2/helmtemplate/"
cp ./HelmTemplate "$HOME/.config/kustomize/plugin/helm-template.webwur.st/v1alpha2/helmtemplate/HelmTemplate"

kustomize build --enable_alpha_plugins ./tests

```


see: https://github.com/kubernetes-sigs/kustomize/blob/master/plugin/someteam.example.com/v1/chartinflator/ChartInflator



## Development

```bash
docker build -t local/helm-template .

docker run -ti \
  -v $PWD:/$PWD -w $PWD \
  local/helm-template \
    HelmTemplate.yaml
```

FIXME remove poetry. just use requirements.txt + tools

```bash
# add a python package to pyproject.toml
docker run -ti -v $PWD:$PWD -w $PWD -- local/helm-template \
  poetry add --dev git+https://github.com/hjacobs/pytest-kind@master

# update package versions in pyproject.toml
docker run -ti -v $PWD:$PWD -w $PWD -- local/helm-template \
  poetry update
```
