#!/usr/bin/env python
"""Wrapper to run Streamlit app with NumPy warnings suppressed at import time."""

import os
import sys
import warnings

# Set environment variables to suppress NumPy build warnings
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

# Suppress the warnings before any imports
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.simplefilter('ignore')

# Now import and suppress NumPy's internal issues
try:
    import numpy as np
    np.seterr(all='ignore')
except:
    pass

# Run Streamlit
import streamlit.cli as stcli

sys.argv = ['streamlit', 'run', 'app/app.py']
sys.exit(stcli.main())
