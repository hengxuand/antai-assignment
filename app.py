from flask import Flask, jsonify, request
import sqlite3
import json
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from flask.helpers import send_from_directory

app = Flask(__name__)
db = 'antai.db'
email_template = "Dear {username},\n\nThank you for your registration. Your member id is {memberId}. Hope you enjoy our web services!\n\nBest,\nAntai Global Inc."


@app.route('/api/member', methods=['GET'])
def load_members():
    try:
        items = request.args.get('items', default=5, type=int)
        page = request.args.get('page', default=1, type=int)
        offset = (page-1) * items
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            result = cur.execute(
                "select * from members limit ? offset ?", (items, offset))
            items = [
                dict(zip([key[0] for key in cur.description], row))
                for row in result
            ]
            cur.close()
            return json.dumps(items)
    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


@app.route('/api/member', methods=['POST'])
def create_member():
    print("Add new member")
    try:
        username = request.form.get('username', default="", type=str)
        email = request.form.get('email', default="", type=str)
        print("add {a} with email {b} .".format(a=username, b=email))
        if username == "" and email == "":
            return jsonify(status='fail', message="need username and email")
        else:
            with sqlite3.connect(db) as conn:
                cur = conn.cursor()
                cur.execute(
                    "insert into members (username, email) values (?, ?)", (username, email))

                conn.commit()
                cur.close()
                return jsonify(status='success', message=username + ' has been added.')
    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


@ app.route('/api/member', methods=['PATCH'])
def update_member():
    print("update a member")
    try:
        member_id = request.form.get('id', default=0, type=int)
        username = request.form.get('username', default="", type=str)
        email = request.form.get('email', default="", type=str)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            agent = cur.execute(
                "select * from members where id = ?", (member_id,)).fetchall()
            if len(agent) == 0:
                cur.close()
                print("{a} not exists.".format(a=member_id))
                return jsonify(status='fail', message=str(member_id) + ' not exists.')
            else:
                cur.execute(
                    "update members set username = ?, email = ? where id = ?", (username, email, member_id))
                print("{a} is updated.".format(a=member_id))
                conn.commit()
                cur.close()
                return jsonify(status='success', message=str(member_id) + ' has been updated.')

    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


@ app.route('/api/member', methods=['DELETE'])
def delete_member():
    print("delete a member")
    try:
        member_id = request.form.get('id', default=0, type=int)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            agent = cur.execute(
                "select * from members where id = ?", (member_id,)).fetchall()
            if len(agent) == 0:
                cur.close()
                print("{a} not exists.".format(a=member_id))
                return jsonify(status='fail', message=str(member_id) + ' not exists.')
            else:
                cur.execute(
                    "delete from members where id = ?", (member_id,))
                print("{a} is deleted.".format(a=member_id))
                conn.commit()
                cur.close()
                return jsonify(status='success', message=str(member_id) + ' has been deleted.')
    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


@ app.route('/api/search', methods=['GET'])
def search_member():
    print("search by username")
    try:
        term = request.args.get('term', default='', type=str)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            search_query = "select * from members where username like ?"
            result = cur.execute(search_query, ('%' + term + '%',))
            items = [
                dict(zip([key[0] for key in cur.description], row))
                for row in result
            ]
            print(items)
            cur.close()
            return json.dumps(items)
    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


@ app.route('/api/greeting', methods=["POST"])
def greeting():
    print("send email")
    try:
        member_id = request.form.get('id', default=0, type=int)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            agent = cur.execute(
                "select * from members where id = ?", (member_id,)).fetchall()
            cur.close()
            if len(agent) == 0:
                return jsonify(status='fail', message=str(member_id) + ' not exists.')
            else:
                member_username = agent[0][1]
                target_email = agent[0][2]
                print(email_template.format(
                    username=member_username, memberId=member_id))
                message = Mail(from_email='hx.d@outlook.com',
                               to_emails=target_email,
                               subject="Greeting from Antai Global Inc.",
                               plain_text_content=email_template.format(username=member_username, memberId=member_id))
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e)
                    return jsonify(status='fail', message=e)

                return jsonify(status='success', message="Greeting email sent to " + member_username)
    except Exception as e:
        print(e)
        return jsonify(status='fail', message=e)


# run the app.
if __name__ == "__main__":
    app.run(debug=True)
