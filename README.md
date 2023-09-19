![Adobe Firefly generated logo. "Ensembl" word rendered with DNA double helices](https://github.com/Tiffany8/ensembl/blob/55a5c599a836f5ad00b0e3a23b30280426307f05/images/ensemquery.png)

# Introduction
EnsemQuery is a command line tool that serves as a convenient interface for fetching and saving specific genetic data points from Ensembl endpoints. Designed with extensibility in mind, the tool is currently focused on the VEP endpoint but aims to incorporate other Ensembl services in the future. It's a useful utility for researchers, healthcare professionals, and anyone interested in genetic data analysis.


# How to Install
## Prerequisites
- Python 3.10 or higher
- [Poetry](https://www.python-poetry.org) for dependency management

## Installation Steps

### From source code
1. Clone the repository:

```bash
git clone git@github.com:Tiffany8/EnsemQuery.git
```

2. Navigate to the project directory:

```bash
cd EnsemQuery
```

3. Install the package using Poetry:

```bash
poetry install
```

4. Activate the virtual environment:

```bash
poetry shell
```

5. Now you can run the CLI tool:

```bash
eqry --help
```

### Directly from private repo
1. This only works if you don't have 2fa setup on your github account (though, I do recomend 2fa setup 😅)
```bash
poetry add git+https://[username]:[password]@github.com/tiffany8/EnsemQuery.git
```


## 👩‍🍳 Cookbook

#### See available commands
```bash
eqry --help

```
** Note: currently only one, vep, is available

#### See available variant consequences subcommands
```bash
eqry vep --help
```

#### Get variant consequences from ids (Note: a variants.txt can be found [here](https://github.com/Tiffany8/EnsemQuery/blob/7ba6757c9b1dcc78d14f13e052e1ac1eaae0d06d/tests/mock-data/variants.txt))
```bash
eqry vep ids variants.txt
```

#### Get variant consequences from ids with custom output file name
```bash
eqry vep ids variants.txt --output-fn mycustomfilename.tsv
```

#### Get variant consequences from ids with custom output file name and output directory
```bash
eqry vep ids variants.txt --output-fn=mycustomfilename.tsv --output-dir=/complete/path/to/existing/folder
```

## Developer Notes

### Testing

1. Setup environment
```bash
poetry shell
poetry install
```
2. Run tests

- To run all tests (note '-s' flag needed to for stdout)
```bash
pytest -s
```

- To run unittests
```bash
pytest -m "not e2e"
```

- To run e2e tests
```bash
pytest -m e2e -s
```

### Development kanban
This is my [kanban](https://tiffanys.notion.site/9bd47681e3ef4ec3b0a2d5566b106ae9?v=8e496ab0cdc14a0b8f51c0fda0e1a68a&pvs=4) I used to track work (link expires 9/26/23).