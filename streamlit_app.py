import streamlit as st
import requests
import collections
import re

# Cached version of requests.get
_CACHED_GET = st.cache(requests.get)

# This struct lets us sort tags by version
_VERSION_FIELDS = ['major', 'minor', 'revision']
StreamlitVersion = collections.namedtuple('StreamlitVersion', _VERSION_FIELDS)

#################
# API Functions #
#################

def get_json(url, **kwargs):
    """Get a URL and parse the response as JSON."""
    response = _CACHED_GET(url, **kwargs)
    response.raise_for_status()
    return response.json()

def get_from_github(get, params={}):
    """Gets some JSON from the Github API server."""
    assert not get.startswith('/')
    url = 'https://api.github.com/' + get
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
    }
    return get_json(url, headers=headers, params=params)

def get_tags():
    """Returns the tags for the Streamlit repo."""
    # Get the tags from github.
    tags = get_from_github(f'repos/streamlit/streamlit/tags')

    # Add a version object to each tag by parsing the "name" field.
    version_expression = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<revision>\d+)')
    for tag in tags:
        match = version_expression.match(tag['name'])
        version = StreamlitVersion(**{name: int(match.group(name)) for name in _VERSION_FIELDS})
        tag['version'] = version
    
    # All done!
    return tags

def get_commit(sha):
    """Returns a commit object from Streamlit for the given SHA."""
    commit = get_from_github(f'repos/streamlit/streamlit/commits/{sha}')
    return commit

def get_commits(start_date, end_date):
    """Returns all the commits on the given interval."""
    # payload = {'since': start_date, 'until': end_date}
    payload = {}
    commits = get_from_github('repos/streamlit/streamlit/commits', params=payload)
    return commits

def get_commit_date(commit):
    """Returns the date from a commit JSON object."""
    return commit['commit']['author']['date']

def get_commit_sha(commit):
    """Returns the date from a commit JSON object."""
    return commit['sha']


#################
# GUI Functions #
#################

def select_tag(label, tags):
    """Creates a widget that lets the user select a tag from a list."""
    # This type lets us sort by version number.
    tags = sorted(tags, key=lambda tag: tag['version'], reverse=True)
    return st.selectbox(label, tags, format_func=lambda tag: tag['name'])

def old_main():
    """Main String."""

    # Dipslay the header
    """# Streamlit Release Notes App"""
    tags = get_tags()    
    tag_1 = select_tag('Starting Version', tags)
    tag_2 = select_tag('Ending Version', tags)
    
    # Get the commits.
    sha_1 = tag_1['commit']['sha']
    sha_2 = tag_2['commit']['sha']
    commit_1 = get_commit(sha_1)
    commit_2 = get_commit(sha_2)

    # commit_1

    # Extract the commit dates
    date_1 = get_commit_date(commit_1)
    date_2 = get_commit_date(commit_2)

    f"""
    Finding commits between `{date_1}` (`{sha_1}`) and `{date_2}` (`{sha_2}`)...
    """
    commits = get_commits(date_1, date_2)
    for i, commit in enumerate(reversed(commits)):
        f'`%05i` : `%s` : `%s`' % (i, get_commit_sha(commit), get_commit_date(commit))

    # commit2 = get_commit(tag1['commit']['sha'])

def main():
    st.write("Let's make a simple app.")
    x = st.slider('x')
    f'${x}^2={x*x}$' 

    if st.button('Show Balloons'):
        st.balloons()

    # # for tag in tags:
    # #     version_string = tag['name']
    # #     f"## {version_string}"
    # #     st.json(tag)

if __name__ == '__main__':
    main()