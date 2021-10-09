import os
from dotenv import load_dotenv
from ssl import SSLContext, PROTOCOL_TLSv1_2

from flask import Flask, redirect, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint, oauth_authorized

load_dotenv()

context = SSLContext(PROTOCOL_TLSv1_2)
context.load_cert_chain('cert/cert.crt', 'cert/server_secret.key')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
blueprint = OAuth2ConsumerBlueprint(
    "github",
    __name__,
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    scope="public_repo,read:org",
    redirect_url ="/github_authorized",
    base_url="https://api.github.com/",
    token_url="https://github.com/login/oauth/access_token",
    authorization_url="https://github.com/login/oauth/authorize",
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    return redirect(url_for("github.login"))


@app.route("/github_authorized")
def github_authorized():
    return "GitHub Authorized!"


@oauth_authorized.connect_via(blueprint)
def authorized(blueprint, token):
    print("authorized() is called.")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        ssl_context=context,
        threaded=True,
        debug=True,
    )
