from flask import Flask,redirect,url_for,render_template,request
from flaskext.mysql import MySQL
from datetime import datetime

app= Flask(__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'smx25ob'
app.config['MYSQL_DATABASE_DB'] = 'crud_python'
mysql.init_app(app)

app=Flask(__name__)


#index page
@app.route('/',methods=['GET','POST'])
def index():

    sql = "SELECT * FROM `empleados`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados )

#eliminar
@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

#editar
@app.route('/edit/<int:id>')
def edit(id):

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `empleados` WHERE id=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()

    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():

    _nombre=request.form["txtNombre"]
    _correo=request.form["txtCorreo"]
    _foto=request.files["txtFoto"]
    id=request.form["txtID"]

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"

    datos=(_nombre,_correo,id)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

#create page
@app.route('/create')
def method_name():
   return render_template('empleados/create.html')


#save data
@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form["txtNombre"]
    _correo=request.form["txtCorreo"]
    _foto=request.files["txtFoto"]

    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)


    sql = "INSERT INTO `empleados`(`id`, `nombre`, `correo`, `foto`) VALUES (NULL,%s,%s,%s)"
    
    datos=(_nombre,_correo,_foto.filename)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('empleados/index.html')
   

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)