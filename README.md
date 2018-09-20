# P3D

Proof of Weak Hands in ONT

## Prepare-Install neo-boa

Note here that the official installation instruction is a little bit misunderstanding. Here I will give the full and correct installation guide.

### 1. Download  [neo-boa](https://github.com/ontio/neo-boa)

### 2. Make a Python 3 virtual environment and activate it (in windows system) via:

```
python3 -m venv venv
cd venv/bin
activate
```
### 3. Then, install the requirements:

```
pip install -r requirements.txt
```

###4. Installation requires a Python 3.6 or later environment.

```
pip install neo-boa
```

### 5. You can read the [docs](https://neo-boa.readthedocs.io/en/latest/) about how to use neo-boa

Don't use boa-test since some of the paths are configured wrongly.

### 6. Run test_compile.py

### 7. Run your ontology testmode, then you can deploy the contract through .avm file

#### Notes
 
 This project is compiled using neo-boa, make sure the folder 'contracts' is under the 'neo-boa-master' folder.
 
 
