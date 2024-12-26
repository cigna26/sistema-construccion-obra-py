import pymysql
from tabulate import tabulate
from pwinput import pwinput
from hashlib import md5
import time
from fpdf import FPDF
from datetime import datetime
# Instalaciones:
# pip install pymysql
# pip install fpdf
# pip install pwinput
# pip install mysql.connector
# pip install tabulate

from os import system



class DataBaseMD5():
    def __init__(self):
        self.conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='carlos123',
            database='certamen'
        )
        self.cursor = self.conexion.cursor()

    def cerrarDB(self):
        self.cursor.close()
        self.conexion.close()

    def login(self):
        nombre = input('Ingrese nombre del usuario = ')
        password = pwinput('Ingrese password = ')
        passwordEnc = md5(password.encode('utf-8')).hexdigest()
        return nombre, passwordEnc
    
    def crearUsuario(self):
        nom,passw = self.login()
        sql1='select * from usuarios where nombre='+repr(nom)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result==None:
                sql2='insert into usuarios values('+repr(nom)+','+repr(passw)+')'
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print('Usuario creado exitosamente')
                except Exception as err:
                    self.conexion.rollback()
                    print("Error al intentar crear el usuario:", err)
            else:
                print('Ya existe ese nombre de usuario')
        except Exception as err:
            print("Error al verificar si el usuario ya existe:", err)

    def ingresar(self):
        nom,passw = self.login()
        sql1='select * from usuarios where nombre='+repr(nom)+' and password = '+repr(passw)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result is not None:
                
                print("Ingreso exitoso, accediendo al menú general...")
                time.sleep(1) 

                
                #Bucle menu
                while True:
                    elige = input('\n Elije una opcion: \n\
                        \t Menu Constructoras(c)\n\
                        \t Menu Obras(o)\n\
                        \t Fin(f)\n\
                        \t ==> \n ').lower()
                    #Si elige la opcion de menu constructoras
                    if elige == 'c':
                        self.menu_constructoras()
                    #Si elige la opcion de menu obras
                    elif elige == 'o':
                        self.menu_obras()
                        
                    elif elige == 'f':
                        print('Fin. Saliendo al Login de usuario')
                        time.sleep(1)
                        break
                    else:
                        print('Error de opción, elija una opcion valida')    
                    input('Pulse Enter para continuar...')
                    system('cls')

            else:
                print('Usuario o contraseña incorrectos. Intente nuevamente.')
        except Exception as err:
            print("Error al verificar usuario:", err)
            self.menu_principal()


#Constructora

    #Lista
    def list_constructoras(self): 
        sql = 'select * from constructoras'
        try:
            self.cursor.execute(sql)
            repu = self.cursor.fetchall()
            print((
            f"{'ID Constructora':10}"
            f"{'Fono ':20}"
            f"{'Email ':12}"
            ))
            for rep in repu:
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:12}")
        except Exception as err:
            print(err)
            
    #CREATE
    def create_constructora(self):
        id_constructora = input('Ingrese ID de la constructora= \n')
        
        #if not id_constructora.isalnum() or len(id_constructora) != 10:
        #    raise ValueError("El código debe ser un valor alfanumérico de exactamente 10 caracteres.")
        
        sql1 = 'select idConstructora from constructoras where idConstructora ='+repr(id_constructora)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() == None:
                fono = input('Fono = \n') 
                email = input('Email \n')
                sql2 = "insert into constructoras values("+repr(id_constructora)+","+repr(fono)+","+repr(email)+")"
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()  
                    print("Constructora creada exitosamente") 
                except Exception as err:
                    self.conexion.rollback()
                    print("Error al crear la constructora:", err)
            else:
                print("Ya existe una constructora con este ID. No se puede crear la constructora.")
        except Exception as err:
            print("Error al verificar el ID de la constructora:", err)  
            
    #READ
    def read_constructora(self):    
        id_buscar = input('Ingrese ID de constructora a buscar = \n')
    
        sql = 'select * from constructoras where idconstructora = '+repr(id_buscar) 
        #repr agrega cremillas al cod
        try:
            self.cursor.execute(sql)
            rep = self.cursor.fetchone()
            if rep is not None:
                print((
                f"{'ID Constructora':10}"
                f"{'Fono ':20}"
                f"{'Email ':12}"
                ))
                
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:12}")
            else:
                print('Id no existe en la base de datos')
        except Exception as err:
            print("Error al realizar la consulta", err) 
            
    #UPDATE
    def update_constructoras(self):
        #Llamar una funcion dentro de otra
        self.list_constructoras()
        
        id_buscar = input('Ingrese ID de constructora que desea actualizar = \n')
        sql1 = 'select * from constructoras where idconstructora='+repr(id_buscar)
        try:
            self.cursor.execute(sql1)
            rep=self.cursor.fetchone()
            if rep!= None:
                print("Información actual de la constructora:")
                print("---------------------------------------------------------")
                print((
                    f"{'ID Constructora':20}"
                    f"{'Fono ':20}"
                    f"{'Email ':12}"
                    ))
                print(f"{rep[0]:20}{rep[1]:20}{rep[2]:12}")
                print("---------------------------------------------------------")
                ##Da la opcion de elegir que desea modificar
                elige=input('\n Que desea modificar?\n fono(f)\n email(e)\n').lower()
                if elige=='f':
                    campo='fono'
                    nuevo=input('Ingrese nuevo fono = ')
                    print("Fono actualizado exitosamente.")
                if elige=='e':
                    campo='email'
                    nuevo=input('Ingrese nuevo email = ')
                    print("Email actualizado exitosamente.")

                sql2 = 'update constructoras set '+campo+'='+repr(nuevo)+' where idconstructora='+repr(id_buscar)
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print("Actualización realizada con éxito.")
                except Exception as err:
                    self.conexion.rollback()
                    print("No existe una constructora con ese ID. Intente con otro ID")
            else:
                print('No existe ese código')
        except Exception as err: 
            print("Error al buscar la constructora:", err)
            
    #DELETE        
    def delete_constructora(self):
        #Llamar una funcion dentro de otra
        self.list_constructoras()
        
        id_buscar = input('Ingrese ID de constructora que desea eliminar = \n')
        sql1 = 'select * from constructoras where idconstructora='+repr(id_buscar)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() != None:
                print("------------------------------------------------")
                print("La constructora con ID", id_buscar, "existe. Verificando si está asociada con alguna obra...")
                print("------------------------------------------------")
                sql2 = 'select * from obras where idConstructora ='+repr(id_buscar)
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone()!= None:
                        time.sleep(1)
                        print('No se puede eliminar, porque esta asociada con Obras')
                    else:
                        sql3 = 'delete from constructoras where idconstructora='+repr(id_buscar)
                        try:
                            self.cursor.execute(sql3)
                            self.conexion.commit()
                            time.sleep(1)
                            print("Constructora eliminada exitosamente.")
                        except Exception as err:
                            self.conexion.rollback()
                            time.sleep(1)
                            print("Error al eliminar la constructora:", err)
                except Exception as err:
                    time.sleep(1)
                    print("Error al verificar las obras asociadas:", err)
            else:
                print("No existe una constructora con este ID. Intente con otro ID")
        except Exception as err:
            print("Error al buscar la constructora:", err)
            
    #Menu para ser llamado en DataBaseMD5 
    def menu_constructoras(self):
        while True:
            elige = input('\n Elije una opcion: \n\
                        \t Listar Constructoras(l)\n\
                        \t Buscar una Constructora(b)\n\
                        \t Crear una Constructora(c)\n\
                        \t Actualizar una Constructora(a)\n\
                        \t Eliminar una Constructora(e)\n\
                        \t Fin(f)\n\
                        \t ==> \n ').lower()
            #Si elige una opcion de CRUD
            if elige == 'l':
                self.list_constructoras()
            elif elige == 'c':
                self.create_constructora()
            elif elige == 'b':
                self.read_constructora()  
            elif elige == 'a':
                self.update_constructoras()
            elif elige == 'e':
                self.delete_constructora()
            elif elige == 'f':
                print('Fin')
                self.cerrarBD()
                break
            else:
                print('Error de opción')
            input('Pulse Enter para continuar...')
            system('cls')
            
            
#OBRAS
    def generar_pdf(self, registros):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Título
            pdf.cell(200, 10, txt="Listado de Obras", ln=True, align="C")

            # Encabezados
            encabezados = ["Cod Obra", "Id Construct.", "Desc Obra", "Estado", "Fecha inicio"]
            for encabezado in encabezados:
                pdf.cell(40, 10, txt=encabezado, border=1)
            pdf.ln()

            # Contenido
            for registro in registros:
                for campo in registro:
                    pdf.cell(40, 10, txt=str(campo), border=1)
                pdf.ln()

            # Guardar el archivo
            pdf.output("listado_obras.pdf")
            print("PDF generado: listado_obras.pdf")
        
    def list_obras(self): 
        sql = 'select * from obras'
        try:
            self.cursor.execute(sql)
            repu = self.cursor.fetchall()

            # Encabezados en consola
            print((
                f"{'Cod. Obra ':10}"
                f"{'Id Construct. ':20}"
                f"{'Descrip. Obra ':20}"
                f"{'Costo Obra ':12}"
                f"{'Fecha Inicio ':12}"
            ))

            # Imprimir registros en consola
            for rep in repu:
                print(f"{rep[0]:12}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")

            # Preguntar si se desea generar el PDF
            opcion = input("Desea generar un PDF con este listado? (s/n): ").lower()
            if opcion == 's':
                self.generar_pdf(repu)

        except Exception as err:
            print("Error al listar obras:", err)
            
        # sql = 'select * from obras'
        # try:
        #     self.cursor.execute(sql)
        #     repu = self.cursor.fetchall()
        #     print((
        #     f"{'Cod. Obra ':10}"
        #     f"{'Id Construct. ':20}"
        #     f"{'Descrip. Obra ':20}"
        #     f"{'Costo Obra ':12}"
        #     f"{'Fecha Inicio ':12}"
        #     ))
        #     for rep in repu:
        #         print(f"{rep[0]:12}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
        # except Exception as err:
        #     print(err)
            
    #CREATE
    def create_obras(self):
        codigo_obra = input('Ingrese ID de la Obra = \n')
        sql1 = 'select codigoObra from obras where codigoObra =' + repr(codigo_obra)

        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone() is None:
                # Pedir el ID de la Constructora
                id_constructora = input('Ingrese ID de la Constructora = \n')
                sql2 = 'select idConstructora from constructoras where idConstructora =' + repr(id_constructora)
                
                
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone() is not None:  # Si el id_constructora existe
                        print("---------------------------------------------")
                        print("Validación de ID de la constructora correcta.")
                        print("---------------------------------------------")

                        descripcionObra = input('Descripcion de la obra = \n')
                        costo = int(input('Costo de la Obra = \n'))
                        fechaInicio = input('Fecha de inicio Obra (aaaa-mm-dd) = \n')

                        # Validar y formatear la fecha
                        try:
                            fecha_inicio = datetime.strptime(fechaInicio, '%Y-%m-%d')
                            fecha_inicio_sql = fecha_inicio.strftime('%Y-%m-%d')
                        except ValueError:
                            print("Formato de fecha incorrecto. Debe ser aaaa-mm-dd.")
                            return
                        
                        print("---------------------------------------------")
                        print("Preparando para insertar en la base de datos...")
                        # Insertar en la base de datos
                        sql3 = "insert into obras (codigoObra, idConstructora, descripcionobra, costo, fechainicio) VALUES (" \
                            + repr(codigo_obra) + ", " + repr(id_constructora) + ", " + repr(descripcionObra) + ", " + repr(costo) + ", " + repr(fecha_inicio_sql) + ")"

                        try:
                            self.cursor.execute(sql3)
                            self.conexion.commit()
                            time.sleep(1) 
                            print("Obra agregada exitosamente...")
                            print("---------------------------------------------")

                        except Exception as err:
                            self.conexion.rollback()
                            print("Error al insertar la obra:", err)
                    else:
                        print("---------------------------------------------")
                        print("El ID de la Constructora no existe. Por favor, verifique y vuelva a intentarlo.")
                        print("---------------------------------------------")

                except Exception as err:
                    print("Error al verificar el ID de la Constructora:", err)
            else:
                print('Ya existe una obra con este ID.')
        except Exception as err:
            print("Error al verificar el código de la obra:", err)

            
            
    #READ
    def read_obras(self):    
        codigo_obra = input('Ingrese codigo a buscar = \n')
    
        sql = 'select * from obras where codigoobra = '+repr(codigo_obra) 
        #repr agrega cremillas al cod
        try:
            self.cursor.execute(sql)
            rep = self.cursor.fetchone()
            if rep is not None:
                print((
                f"{'Codigo Obra':10}"
                f"{'Ide Constructora ':20}"
                f"{'Descripcion ':12}"
                f"{'Costo ':12}"
                f"{'Fecha Inicio':12}"
                ))
                
                print(f"{rep[0]:10}{rep[1]:20}{rep[2]:20}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
            else:
                print('Codigo no existe en la base de datos')
        except Exception as err:
            print("Error al realizar la consulta", err)
            
            
    #UPDATE
    def update_obras(self):
        
        #Llamar una funcion dentro de otra
        self.list_obras()
        
        codigo_obra = input('Ingrese codigo a buscar = \n')
        sql1 = 'select * from obras where codigoobra ='+repr(codigo_obra)
        try:
            self.cursor.execute(sql1)
            rep=self.cursor.fetchone()
            if rep!= None:
                print((
                f"{'Codigo Obra':13}"
                f"{'Id Constructora ':20}"
                f"{'Descripcion':15}"
                f"{'Costo ':12}"
                f"{'Fecha Inicio':12}"
                ))
                
                print(f"{rep[0]:13}{rep[1]:20}{rep[2]:15}{rep[3]:<12}{rep[4].strftime('%d/%m/%Y'):12}")
                elige=input('\n Que desea modificar?\n Descripcion(d)\n Costo(c)\n').lower()
                if elige=='d':
                    campo='descripcionObra'
                    nuevo=input('Ingrese nueva Descripcion=')
                if elige=='c':
                    campo='costo'
                    nuevo=input('Ingrese nuevo costo=')
                

                sql2 = 'update obras set '+campo+'='+repr(nuevo)+' where codigoobra='+repr(codigo_obra)
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print("---------------------------------------------")
                    print("Actualizando la base de datos con modificaciones...")
                    time.sleep(1)
                    print("La obra fue actualizada con éxito.")
                    print("---------------------------------------------")

                except Exception as err:
                    self.conexion.rollback()
                    print("Error al actualizar la obra:", err)
            else:
                print('No existe ese código')
        except Exception as err: 
            print("Error al buscar la obra:", err)
            
    #Menu para ser llamado en DataBaseMD5 
    def menu_obras(self):
        while True:
            elige = input('\n Elije una opcion: \n\
                \t Listar Obras(l)\n\
                \t Buscar una Obra(b)\n\
                \t Crear una Obra(c)\n\
                \t Actualizar una Obra(a)\n\
                \t Fin(f)\n\
                \t ==> \n ').lower()
            #Si elige una opcion de CRUD
            if elige == 'l':
                self.list_obras()
            elif elige == 'c':
                self.create_obras()
            elif elige == 'b':
                self.read_obras()
            elif elige == 'a':
                self.update_obras()
                        
            elif elige == 'f':
                print('Fin')
                self.cerrarBD()
                break
            else:
                print('Error de opción')
            input('Pulse Enter para continuar...')
            system('cls')
    