import time
import uuid
from datetime import date, datetime

import qrcode
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from __init__ import create_app, db
from models import User, event_scan, names

now = datetime.now()
dt = now.strftime("%Y-%m-%d %H:%M:%S")
main = Blueprint('main', __name__)
today = date.today()


# def UID():
#     myuuid = uuid.uuid4()
#     return str(myuuid)


@main.route('/')
def index():
    return render_template('login.html')


@main.route('/scan')
@login_required
def scan():
    if request.is_json:
        result = request.args.get('scan')
        guest = db.session.query(names).filter_by(uid=result).first()
        alert = None
        if guest != None:
            if guest.flag == "0":
                now = datetime.now()
                try:
                    alert = "Welcome "
                    new_scan = event_scan(name=guest.name)
                    db.session.add(new_scan)
                    db.session.commit()
                    db.session.query(names).filter_by(
                        uid=result).update({"flag": 1})
                    db.session.commit()

                except:
                    alert = 'Connection Failed!'
            else:
                alert = 'Pass is Expired! [USED]'
        else:
            alert = 'Pass is Invlid!'

        return jsonify({"alert": alert})
    return render_template('scanner.html')


@main.route('/info', methods=['GET', 'POST'])
@login_required
def Info():
    users = User.query.all()
    scans = event_scan.query.all()
    return render_template('info.html', users=users, scans=scans)


app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
