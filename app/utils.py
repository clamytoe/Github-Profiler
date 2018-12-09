import requests
from flask import current_app

from app import db
from app.models import Accounts, Gists, Repos


def add_gists(user):
    """Adds gists information"""
    url = current_app.config['API_BASE'] + user + '/gists'
    response = requests.get(url)
    etag = response.headers['ETag']
    data = response.json()

    if current_app.config['DEBUG']:
        print(f"Found {len(data)} gists")

    for gist in data:  # gist_id, owner, filename, html_url, description, language, etag
        files = []
        for file in gist['files']:
            files.append(file)
        if current_app.config['DEBUG']: print(f'{len(files)} Files: {files}')
        add_gist = Gists(gist['id'], user, files[0], gist['html_url'], gist['description'], etag)
        db.session.add(add_gist)
        if current_app.config['DEBUG']: print(f'Added gist {files[0]}')
    db.session.commit()

    # Since there might be more than one, a list is used to hold them
    gists = []
    all_gists = Gists.query.all()

    for gist in all_gists:
        if gist.owner == user:
            gists.append(gist)

    if current_app.config['DEBUG']: print(f"Returning {gists}")

    return gists


def add_repos(user):
    """Adds repos information"""
    url = current_app.config['API_BASE'] + user + '/repos'
    response = requests.get(url)
    etag = response.headers['ETag']
    data = response.json()
    if current_app.config['DEBUG']:
        print(f"Found {len(data)} repos")

    for repo in data:  # repos_id, owner, name, html_url, description, fork, language, created_at, updated_at, etag
        add_repo = Repos(repo['id'], user, repo['name'], repo['html_url'], repo['description'], repo['fork'],
                         repo['language'], repo['created_at'], repo['pushed_at'], etag)
        db.session.add(add_repo)
        if current_app.config['DEBUG']: print(f"Added repo {repo['name']}")
    db.session.commit()

    # Since there might be more than one, a list is used to hold them
    repos = []
    all_repos = Repos.query.all()

    for repo in all_repos:
        if repo.owner == user:
            repos.append(repo)

    if current_app.config['DEBUG']: print(f"Returning {repos}")

    return repos


def add_profile(user):
    """Adds account information"""
    url = current_app.config['API_BASE'] + user
    if current_app.config['DEBUG']:
        print(f"Retrieving: {url}")

    # Header info
    response = requests.get(url)
    status = response.headers['Status']
    limit = response.headers['X-RateLimit-Limit']
    remaining = response.headers['X-RateLimit-Remaining']
    reset = response.headers['X-RateLimit-Reset']
    etag = response.headers['ETag']
    if current_app.config['DEBUG']: print(f'Status: {status}')
    if current_app.config['DEBUG']: print(f'Limit: {limit}')
    if current_app.config['DEBUG']: print(f'Remaining: {remaining}')
    if current_app.config['DEBUG']: print(f'Reset: {reset}')
    if current_app.config['DEBUG']: print(f'ETag: {etag}')
    if current_app.config['DEBUG']: print(f"Retrieved: {url}")

    data = response.json()
    if current_app.config['DEBUG']: print(f"Found {data['name']}")

    # add the account
    add_account = Accounts(data['login'].lower(), data['avatar_url'], data['url'], data['html_url'],
                           data['followers_url'], data['following_url'], data['gists_url'], data['starred_url'],
                           data['subscriptions_url'], data['organizations_url'], data['repos_url'], data['events_url'],
                           data['received_events_url'], data['name'], data['company'], data['blog'], data['location'],
                           data['email'], data['hireable'], data['bio'], data['public_repos'], data['public_gists'],
                           data['followers'], data['following'], data['created_at'], data['updated_at'], etag)
    db.session.add(add_account)
    db.session.commit()

    account = Accounts.query.get(user)
    if current_app.config['DEBUG']: print(f"Returning {account}")

    return account


def check_etag(user, old_etag):
    """Compares the etag from the db to the ones from GitHub"""
    url = current_app.config['API_BASE'] + user
    response = requests.head(url)
    new_etag = response.headers['ETag']
    matched = True if old_etag == new_etag else False
    if current_app.config['DEBUG']:
        print(f'ETags Match: {matched}')

    return matched
