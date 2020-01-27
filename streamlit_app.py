import streamlit as st
import requests
import collections
import re

# Cached version of requests.get
_CACHED_GET = st.cache(requests.get)

# This struct lets us sort tags by version
_VERSION_FIELDS = ['major', 'minor', 'revision']
StreamlitVersion = collections.namedtuple('StreamlitVersion', _VERSION_FIELDS)


def get_json(url, **kwargs):
    """Get a URL and parse the response as JSON."""
    response = _CACHED_GET(url, **kwargs)
    response.raise_for_status()
    return response.json()

def get_from_github(get):
    """Gets some JSON from the Github API server."""
    assert not get.startswith('/')
    url = 'https://api.github.com/' + get
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
    }
    return get_json(url, headers=headers)

def parse_tag(tag):
    version_name = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<revision>\d+)')
    match = version_name.match(tag['name'])
    version = StreamlitVersion(**{name: match.group(name) for name in _VERSION_FIELDS})
    return (version, tag)

def select_tag(label, tags):
    """Creates a widget that lets the user select a tag from a list."""
    # This type lets us sort by version number.
    tags = sorted(map(parse_tag, tags))
    version, selected_tag = st.selectbox(label, tags, format_func=lambda tag: tag[1]['name'])
    return selected_tag

def main():
    """Main String."""

    # Dipslay the header
    """# Streamlit Release Notes App"""
    # get the tag
    tags = get_from_github(f'repos/streamlit/streamlit/tags')
    tag1 = select_tag('First Tag', tags)
    tag1


    # for tag in tags:
    #     version_string = tag['name']
    #     f"## {version_string}"
    #     st.json(tag)

if __name__ == '__main__':
    main()