from fakepinterest import database, app
from fakepinterest.models import Usuario, Postagem

with app.app_context():
    database.create_all()