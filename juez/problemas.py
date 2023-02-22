import os
import juez.evaluador
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from juez.auth import login_required
from juez.db import get_db

bp = Blueprint('problemas', __name__)
ALLOWED_EXTENSIONS = {'py'}
UPLOAD_FOLDER="./uploads"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    ids=juez.evaluador.lista_problemas()
    problemas=[]
    for id in ids:
        problemas.append(juez.evaluador.lee_problema(id))

    return render_template('problemas/index.html', problemas=problemas)

@bp.route('/<string:id>/resolver', methods=('GET', 'POST'))
def resolver(id):
    resultado_evaluacion=""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No has seleccionado ningún fichero')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No has seleccionado ningún fichero')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('El fichero no es Python')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath=os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        resultado_evaluacion=juez.evaluador.evalua_problema(id,filepath)

        os.remove(filepath)

    return render_template('problemas/resolver.html', problema=juez.evaluador.lee_problema(id), resultado=resultado_evaluacion)