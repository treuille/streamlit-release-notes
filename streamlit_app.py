import streamlit as st
import numpy as np

"""
# Hello Coatue
"""

if st.button('Show some balloons'):
    st.balloons()

nrows = st.slider('rows', 0, 10000, 200)
'random data', np.random.randn(nrows, nrows)