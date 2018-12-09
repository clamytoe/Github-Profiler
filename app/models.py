from app import db


class Accounts(db.Model):
    """Accounts schema"""
    login = db.Column(db.String(20), primary_key=True)
    avatar_url = db.Column(db.String(80))
    url = db.Column(db.String(50))
    html_url = db.Column(db.String(50))
    followers_url = db.Column(db.String(80), default=None)
    following_url = db.Column(db.String(80), default=None)
    gists_url = db.Column(db.String(80), default=None)
    starred_url = db.Column(db.String(80), default=None)
    subscriptions_url = db.Column(db.String(80), default=None)
    organizations_url = db.Column(db.String(80), default=None)
    repos_url = db.Column(db.String(80), default=None)
    events_url = db.Column(db.String(80), default=None)
    received_events_url = db.Column(db.String(80), default=None)
    name = db.Column(db.String(40))
    company = db.Column(db.String(40), default=None)
    blog = db.Column(db.String(50), default=None)
    location = db.Column(db.String(40), default=None)
    email = db.Column(db.String(40), default=None)
    hireable = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, default=None)
    public_repos = db.Column(db.Integer, default=0)
    public_gists = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(20))
    updated_at = db.Column(db.String(20))
    etag = db.Column(db.String(32))

    def __init__(self, login, avatar_url, url, html_url, followers_url, following_url, gists_url, starred_url,
                 subscriptions_url, organizations_url, repos_url, events_url, received_events_url, name, company,
                 blog, location, email, hireable, bio, public_repos, public_gists, followers, following, created_at,
                 updated_at, etag):
        self.login = login
        self.avatar_url = avatar_url
        self.url = url
        self.html_url = html_url
        self.followers_ur = followers_url
        self.following_url = following_url
        self.gists_url = gists_url
        self.starred_url = starred_url
        self.subscriptions_url = subscriptions_url
        self.organizations_url = organizations_url
        self.repos_url = repos_url
        self.events_url = events_url
        self.received_events_url = received_events_url
        self.name = name
        self.company = company
        self.blog = blog
        self.location = location
        self.email = email
        self.hireable = hireable
        self.bio = bio
        self.public_repos = public_repos
        self.public_gists = public_gists
        self.followers = followers
        self.following = following
        self.created_at = created_at
        self.updated_at = updated_at
        self.etag = etag

    def __repr__(self):
        return f'<GHAccount {self.name} ({self.login})>'


class Repos(db.Model):
    """Repos schema"""
    repos_id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(20), db.ForeignKey('accounts.login'))
    name = db.Column(db.String(40))
    html_url = db.Column(db.String(50))
    description = db.Column(db.Text, default=None)
    fork = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(20))
    created_at = db.Column(db.String(20))
    pushed_at = db.Column(db.String(20))
    etag = db.Column(db.String(32))

    def __init__(self, repos_id, owner, name, html_url, description, fork, language, created_at, pushed_at, etag):
        self.repos_id = repos_id
        self.owner = owner
        self.name = name
        self.html_url = html_url
        self.description = description
        self.fork = fork
        self.language = language
        self.created_at = created_at
        self.pushed_at = pushed_at
        self.etag = etag

    def __repr__(self):
        return f'<Repo {self.owner}: {self.name}>'


class Gists(db.Model):
    """Gists schema"""
    gist_id = db.Column(db.String(32), primary_key=True)
    owner = db.Column(db.String(20), db.ForeignKey('accounts.login'))
    filename = db.Column(db.String(40))
    html_url = db.Column(db.String(50))
    description = db.Column(db.Text, default=None)
    etag = db.Column(db.String(32))

    def __init__(self, gist_id, owner, filename, html_url, description, etag):
        self.gist_id = gist_id
        self.owner = owner
        self.filename = filename
        self.html_url = html_url
        self.description = description
        self.etag = etag

    def __repr__(self):
        return f'<Gist {self.owner}: {self.filename}>'

