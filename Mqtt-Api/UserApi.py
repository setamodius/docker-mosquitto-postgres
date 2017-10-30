from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import hashing_passwords as hp
import dbmanager
import Model

app = FlaskAPI(__name__)
# dbhost = "postgres-mosq"
dbhost = "10.3.4.241"
myDb = dbmanager.Connection(dbhost, "postgres", 5432, "postgres", "password")


def user_repr(username):
    result_user = get_user(username)
    if result_user is None:
        raise exceptions.NotFound()
    return {
        'url': request.host_url.rstrip('/') + url_for('user_detail', username=result_user.username),
        'name': result_user.name,
        'username': result_user.username,
        'privileges': result_user.privileges
    }


@app.route("/users/", methods=['GET', 'POST'])
def users_list():
    """
    List or create users
    """
    if request.method == 'POST':
        new_user_name = str(request.data.get('username', ''))
        new_password = str(request.data.get('password', ''))
        full_name = str(request.data.get('name', ''))
        privileges = str(request.data.get('privileges', ''))
        if get_user(new_user_name) is not None:
            return '', status.HTTP_406_NOT_ACCEPTABLE
        hashed_password = hp.make_hash(new_password)
        row_count = myDb.execute_rowcount(
            "INSERT INTO users(username, password, name, privilege, super) VALUES(%s, %s, %s, %s, 0)",
            new_user_name, hashed_password, full_name, privileges)
        if row_count > 0:
            myDb.commit()
        return user_repr(new_user_name), status.HTTP_201_CREATED

    # request.method == 'GET'
    result_user = myDb.query("SELECT username FROM users")
    return [user_repr(user['username']) for user in result_user]


@app.route("/users/<string:username>/", methods=['GET', 'PUT', 'DELETE'])
def user_detail(username):
    """
    Retrieve, update or delete users.
    """
    if request.method == 'PUT':
        new_password = str(request.data.get('password', ''))
        full_name = str(request.data.get('name', ''))
        privileges = str(request.data.get('privileges', ''))
        if get_user(username) is None:
            return '', status.HTTP_404_NOT_FOUND
        hashed_password = hp.make_hash(new_password)
        row_count = myDb.execute_rowcount(
            "UPDATE users SET password = %s, name = %s, privilege = %s WHERE username = %s;",
            hashed_password, full_name, privileges, username)
        if row_count == 1:
            myDb.commit()
            return user_repr(username), status.HTTP_200_OK
        else:
            return user_repr(username), status.HTTP_409_CONFLICT

    elif request.method == 'DELETE':
        row_count = myDb.execute_rowcount("DELETE FROM users WHERE username = %s", username)
        myDb.commit()
        if row_count > 0:
            return '', status.HTTP_204_NO_CONTENT
        else:
            return '', status.HTTP_404_NOT_FOUND

    # request.method == 'GET'

    return user_repr(username)


def get_user(username):
    result_user = myDb.query("SELECT * FROM users WHERE username = %s", username)
    if len(result_user) == 0:
        return None

    user_data = Model.User()
    user_data.username = result_user[0]["username"]
    user_data.name = result_user[0]["name"]
    user_data.privileges = result_user[0]["privilege"]
    return user_data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
