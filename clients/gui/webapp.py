import requests
from flask import render_template, Blueprint, request, redirect, url_for

from caller import Caller
from diffie_hellman import gen_public_key
from gui.util import get_host, get_dirname_path_parts, get_dir_content, get_path_format
from parsing import Parser

webapp = Blueprint("webapp", __name__)

caller: Caller = None


@webapp.route('/', methods=['GET', 'POST'])
def webapp_login():
    global caller

    # logging in
    if request.method == 'POST':
        host_param = request.form['host']

        try:

            if not Caller.check_up(host_param):
                return render_template("login.html", msg='host is down', host=host_param)

            private_key_df = request.form['private_key']
            private_key_df_derived = Parser.derive(private_key_df)
            public_key_df = gen_public_key(private_key_df_derived)

            caller = Caller(host_param, public_key_df)

            return redirect(url_for('webapp.webapp_main', path='', dirname=''))

        except TypeError as te:
            return render_template("login.html", msg=str(te), host=host_param)

    elif request.method == 'GET':
        if caller is not None:
            if caller.get_session().status_code == 200:
                return redirect(url_for('webapp.webapp_main', path='', dirname=''))

        return render_template("login.html")


@webapp.route('/db', methods=['GET'])
def webapp_main():
    global caller

    if request.method == 'GET':

        # if no caller, redirect to login
        if caller is None:
            return redirect(url_for('webapp.webapp_login'))

        # if session no active anymore
        if caller.get_session().status_code != 200:
            return redirect(url_for('webapp.webapp_login'))

        # get current path content
        path_param = request.args['path']
        dirname_param = request.args['dirname']

        template = "dir_content.html"
        host = get_host(caller.host)

        path_format = path_param.replace('.', '/')
        r = caller.get_directory(path_format, dirname_param)

        dirname, path_parts = get_dirname_path_parts(dirname_param, path_param)

        if r.status_code != 200:
            m = r.json()['message']
            msg = f'failed to get directory: {m}'
            return render_template(
                template, host=host, msg=msg, err=True,
                path_parts=path_parts, dirname=dirname
            )

        dirs = r.json()['body']
        dir_content_list = get_dir_content(dirs, path_param, dirname_param)

        return render_template(
            template, host=host, dir_content_list=dir_content_list,
            path_parts=path_parts, dirname=dirname
        )


@webapp.route('/db/entry', methods=['GET'])
def webapp_entry():
    global caller

    if request.method == 'GET':
        # if no caller, redirect to login
        if caller is None:
            return redirect(url_for('webapp.webapp_login'))

        # if session no active anymore
        if caller.get_session().status_code != 200:
            return redirect(url_for('webapp.webapp_login'))

        # get current path content
        path_param = request.args['path']
        dirname_param = request.args['dirname']
        entry_param = request.args['entry']

        template = "entry.html"
        host = get_host(caller.host)

        dirname, path_parts = get_dirname_path_parts(
            dirname_param, path_param)

        path_format = path_param.replace('.', '/')
        path_format = get_path_format(path_format, dirname_param)
        r = caller.get_entry(path_format, entry_param)
        if r.status_code != 200:
            m = r.json()['message']
            msg = f'failed to get entry: {m}'
            return render_template(
                template, host=host, msg=msg, err=True,
                path_parts=path_parts, dirname=entry_param
            )

        entry = r.json()['body']

        url_dir = f'/db?path={path_param}&dirname={dirname_param}'

        return render_template(
            template, host=host, entry=entry, url_dir=url_dir,
            entry_name=entry_param, path_parts=path_parts,
            dirname=entry_param
        )


@webapp.route('/logout/', methods=['GET'])
def webapp_logout():
    global caller

    if request.method == 'GET':
        # logout
        if caller is not None:
            r = caller.delete_session()
            if r.status_code != 200:
                err = r.json()['message']
                return render_template(
                    "main.html", host=get_host(caller.host), msg=f'failed to logout: {err}'
                )

            caller = None

        return redirect(url_for('webapp.webapp_login'))
