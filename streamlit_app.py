import streamlit as st
import requests

_cached_get = st.cache(requests.get)

def get_json(url, **kwargs):
    """Cached function to get json from Github."""
    response = _cached_get(url, **kwargs)
    response.raise_for_status()
    return response.json()

def get_from_github(get):
    assert not get.startswith('/')
    url = 'https://api.github.com/' + get
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
    }
    return get_json(url, headers=headers)

def main():
    """Main String."""

    # Dipslay the header
    """# Streamlit Release Notes App"""
    # testing some queries
    queries = ['users/treuille', 'orgs/streamlit/repos', 'repos/streamlit/streamlit/tags']
    for query in queries:
        st.write(f'`{query}`')
        st.json(get_from_github(query))

if __name__ == '__main__':
    main()