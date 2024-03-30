from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PUERTO = 27017
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://" + MONGO_HOST + ":" + str(MONGO_PUERTO) + "/"

MONGO_BASEDATOS = "universidad"
MONGO_COLECCION = "alumnos"

cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos = cliente[MONGO_BASEDATOS]
coleccion = baseDatos[MONGO_COLECCION]

ID_ALUMNO = ""

def mostrarDatos(tabla):
    try:
        registros = tabla.get_children()   
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find():
            tabla.insert("", 0, text=documento["_id"], values=(documento["nombre"],))

        cliente.server_info()
        print("Conectado a MongoDB Exitosamente")
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Error de Tiempo: ", errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("falla de conexion: ", errorConexion)


def crearRegistro():
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(rut.get()) != 0:
        try:
            coleccion.insert_one({"nombre": nombre.get(), "sexo": sexo.get(), "rut": rut.get()})
            messagebox.showinfo("Exito", "Registro creado exitosamente")
            nombre.delete(0, END)
            sexo.delete(0, END)
            rut.delete(0, END)
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Error de Tiempo: ", errorTiempo)
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("falla de conexion: ", errorConexion)
    else:
        messagebox.showerror("Error", "Por favor llena todos los campos")
    mostrarDatos(tabla)


def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO = str(tabla.item(tabla.selection())["text"])
    documento = coleccion.find_one({"_id": ObjectId(ID_ALUMNO)})
    nombre.delete(0, END)  
    nombre.insert(0, documento["nombre"])
    sexo.delete(0, END)
    sexo.insert(0, documento["sexo"])
    rut.delete(0, END)
    rut.insert(0, documento["rut"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    eliminar["state"] = "normal"


def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(rut.get()) != 0:
        try:
            coleccion.update_one({"_id": ObjectId(ID_ALUMNO)}, {"$set": {"nombre": nombre.get(), "sexo": sexo.get(), "rut": rut.get()}})
            messagebox.showinfo("Exito", "Registro editado exitosamente")
            nombre.delete(0, END)
            sexo.delete(0, END)
            rut.delete(0, END)
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Error de Tiempo: ", errorTiempo)
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("falla de conexion: ", errorConexion)
    else:
        messagebox.showerror("Error", "Por favor llena todos los campos")
    mostrarDatos(tabla)

    crear["state"] = "normal"
    editar["state"] = "disabled"
    eliminar["state"] = "disabled"
    

def eliminarRegistro():
    global ID_ALUMNO
    if ID_ALUMNO != "":
        try:
            coleccion.delete_one({"_id": ObjectId(ID_ALUMNO)})
            messagebox.showinfo("Exito", "Registro eliminado exitosamente")
            nombre.delete(0, END)
            sexo.delete(0, END)
            rut.delete(0, END)
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Error de Tiempo: ", errorTiempo)
        except pymongo.errors.ConnectionFailure as errorConexion:
            print("falla de conexion: ", errorConexion)
    else:
        messagebox.showerror("Error", "Por favor selecciona un registro")
    crear["state"] = "normal"
    editar["state"] = "disabled"
    eliminar["state"] = "disabled"

    mostrarDatos(tabla)


ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("Nombre",))
tabla.grid(row=1, column=0, columnspan=2)
tabla.heading("#0", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.bind("<Double-Button-1>", dobleClickTabla)

# Nombre
Label(ventana, text="Nombre: ").grid(row=2, column=0)
nombre = Entry(ventana)
nombre.grid(row=2, column=1)

# Sexo
Label(ventana, text="Sexo: ").grid(row=3, column=0)
sexo = Entry(ventana)
sexo.grid(row=3, column=1)

# Rut
Label(ventana, text="Rut: ").grid(row=4, column=0)
rut = Entry(ventana)
rut.grid(row=4, column=1)

# Crear Boton
crear = Button(ventana, text="Crear alumno", command=crearRegistro, bg="green", fg="white")
crear.grid(row=5, column=0, columnspan=2)

# Editar Boton
editar = Button(ventana, text="Editar alumno", command=editarRegistro, bg="yellow", fg="black")
editar.grid(row=6, column=0, columnspan=2)
editar["state"] = "disabled"

# Eliminar Boton
eliminar = Button(ventana, text="Eliminar alumno", command=eliminarRegistro, bg="red", fg="white")
eliminar.grid(row=7, column=0, columnspan=2)
eliminar["state"] = "disabled"





mostrarDatos(tabla)

ventana.mainloop()

