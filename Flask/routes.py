from flask import render_template, redirect, url_for, flash

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html', 
                             title='Bienvenido',
                             message='Aplicación Web Flask')
   