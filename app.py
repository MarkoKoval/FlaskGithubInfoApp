""" flask app to get responses for github requests"""
from flask import Flask
import requests


app = Flask(__name__)
headers = {"Authorization": "Bearer b3e7bb8132901122d4451aaf4121867e5616b38f"}


def run_query(query):
    """ run query to github grapql api responses for specified query """
    try:
        request = requests.post('https://api.github.com/graphql',
                                json={'query': query}, headers=headers)
        return request.json()
    except ConnectionError as connection_exception:
        return connection_exception
    except ValueError as value_exception:
        return value_exception
    except TypeError as type_exception:
        return type_exception


@app.route('/users/<login>', methods=["GET"])
def get_github_name(login):
    """ guery to get github name of user """
    query = """
    query { 
      user(login: "%s") {
        name
      }
    }
    """ % login
    result = run_query(query)
    return {"user": result["data"]["user"], "status": 200 if result["data"]["user"] else 500}


@app.route('/users/<login>/repos/count', methods=["GET"])
def get_github_repos_count(login):
    """ guery to get github user repositories count"""
    query = """
                            query {
                              repositoryOwner (login: "%s") {
                                repositories (ownerAffiliations: OWNER) {
                                  totalCount
                                }
                              }
                            }
                            """ % login

    result = run_query(query)

    if result["data"]["repositoryOwner"] is None:
        return {"result": result, "status": 500}

    return {"count": result["data"]["repositoryOwner"]['repositories']["totalCount"], "status": 200}


@app.route('/users/<login>/repos/info', methods=["GET"])
def get_github_repos_info(login):
    """ guery to get github user repositories info """
    response = get_github_repos_count(login)
    if response["status"] == 200:
        repos_count = response["count"]
    else:
        return {"result": "User not found", "status": 500}

    if repos_count == 0:
        return {"repo_info": [], "status": 200}
    query = """
    query {
      repositoryOwner (login: "%s") {
        repositories(first:%s,ownerAffiliations: OWNER) {
          nodes {
            name,
            url
          }
        }
      }
    }
    """ % (login, repos_count)
    result = run_query(query)
    return {"repo_info": result, "status": 200}


if __name__ == '__main__':
    app.run()
