import requests
from flask import current_app, render_template, request

from app.models import Accounts, Gists, Repos
from app.utils import add_gists, add_profile, add_repos, check_etag

from . import home


@home.route('/')
def index():
    """
    Home page of the app It loads the index template page.
    """
    return render_template('index.html')


@home.route('/user', methods=['POST'])
def get_account():
    """
    Access account
    Attempts to retrieve account info from the database. If the account is found, it checks to see if the online version
    has changed. If it has, the info in the database is removed and the new data is pulled from GitHub. If the account
    does not exist at all in the database, it gets it from GitHub.
    """
    username = request.form['username']
    user = username.lower()
    gh_user = None
    gh_repos = []
    gh_gists = []
    is_account = False
    is_repos = False
    is_gists = False

    if not user:
        return redirect('/')

    # check existing accounts to see if its in there
    accounts = Accounts.query.all()
    for account in accounts:
        if account.login == user:
            if current_app.config['DEBUG']: print(f"User already exists: {account.login}")
            if current_app.config['DEBUG']: print("Checking for updates to info")
            same = check_etag(user, account.etag)
            if same:
                gh_user = account
                if current_app.config['DEBUG']: print(f"Pulling account info from db: {gh_user.login}")
                is_account = True
            else:
                if current_app.config['DEBUG']: print(f'Account etags differ, will have to get an update')
                Accounts.query.filter(Accounts.login == user).delete()
                db.session.commit()
                break

    # add the account if not in database already
    if not is_account:
        url = current_app.config['API_BASE'] + user
        if current_app.config['DEBUG']: print(f"Checking: {url}")
        # Header info
        response = requests.head(url)
        status = response.headers['Status']
        if current_app.config['DEBUG']: print(f'Status: {status}')

        # Handle errors
        if '404' in status:  # 404 Not Found
            return render_template('index.html', error="User not found! Try a different dude!")
        elif '403' in status:  # 403 Forbidden
            remaining = int(response.headers['X-RateLimit-Reset'])
            reset_at = strftime("%H:%M:%S", localtime(remaining))
            return render_template('index.html',
                    error=f"You have exceeded the number of lookups! Come back after {reset_at}!")
        else:
            gh_user = add_profile(user)
            if current_app.config['DEBUG']:
                print(f"Retrived {gh_user}")
            if current_app.config['DEBUG']:
                print(f"Name is {gh_user.name}")
            is_account = True

    if is_account:
        # Check and see if we have a repos for the user
        repos = Repos.query.all()

        for repo in repos:
            if repo.owner == user:
                if not is_repos:
                    # Check to see if the repos in the db are still up to date
                    is_repos = check_etag(user + '/repos', repo.etag)
                    if not is_repos:
                        if current_app.config['DEBUG']:
                            print(f'Repos etags differ, will have to get an update')
                        Repos.query.filter(Repos.owner == user).delete()
                        db.session.commit()
                        break
                else:
                    gh_repos.append(repo)
                    if current_app.config['DEBUG']:
                        print(f"Found existing repo: {repo}")
                    is_repos = True

        # Check and see if we have any gists for the user
        gists = Gists.query.all()

        for gist in gists:
            if gist.owner == user:
                if not is_gists:
                    # Check to see if they are up to date
                    is_gists = check_etag(user + '/gists', gist.etag)
                    if not is_gists:
                        if current_app.config['DEBUG']:
                            print(f'Gist etags differ, will have to get an update')
                        Gists.query.filter(Gists.owner == user).delete()
                        db.session.commit()
                        break
                else:
                    gh_gists.append(gist)
                    if current_app.config['DEBUG']:
                        print(f"Found existing gist: {gist}")
                    is_gists = True

    if not is_repos:
        if current_app.config['DEBUG']:
            print("Repos were not found or needs to be updated")
        gh_repos = add_repos(user)
        if current_app.config['DEBUG']:
            print(f"Repos: {gh_repos}")

    if not is_gists:
        if current_app.config['DEBUG']:
            print("Gists were not found or needs to be updated")
        gh_gists = add_gists(user)
        if current_app.config['DEBUG']:
            print(f"Gists: {gh_gists}")

    return render_template('index.html', gh_user=gh_user, gh_repos=gh_repos, gh_gists=gh_gists)

