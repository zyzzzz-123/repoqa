# RepoQA

## DEV Structure

- `repo`: entrypoint for working repositories
- `repoqa`: source code for the library
  - `curate`: code for dataset curation
  - `evaluate`: code for model evaluation
- `scripts`: scripts for maintaining the repository and other utilities
  - `dev`: scripts for CI/CD and repository maintenance

## Development Beginner Notice

### After clone

```shell
pip install pre-commit
pre-commit install
pip install -r requirements.txt
```

### Import errors?

```shell
# Go to the root path of RepoQA
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
