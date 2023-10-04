# LiamHsieh toolbox

This Python package is a collection of Python utilities for those projects created by Liam Hsieh.  

We recommend using virtual environment.  
Fist activate the virtual environment you want this package to be installed, then run following command to install this package for your venv:
```bash
pip install liamhsieh-toolbox
```
or install from GitHub directly (not recommended)
```bash
pip install git+https://github.com/liam-hsieh/liamhsieh-toolbox.git
```

Please note that all dependencies will be considered while installing toolbox but IBM CPLEX.
You need to install CPLEX for your pyenv venv and then install docplex.

1. Remember to activate your pyenv venv
2. Use the script `setup.py` located in your `$Cplexhome/python` (default is `/opt/ibm/ILOG/<CPLEX_VERSION>/python` on ADOS VM) with command `python setup.py install`
3. install docplex `pip install docplex`

Check [change log](liamhsieh-toolbox/toolbox/change_log) for new features added