import cx_Oracle
from random import randint

################################################################################################################
#################################################################################################################

# Funciones relacionadas con la lectura de la fecha

meses = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07",
         "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

def addDay(date): # Recibe una fecha en formato "MES AAAA" (Sin dia)
    fecha = date.split(" ")
    fecha[0] = meses[fecha[0]]
    dia = str(randint(1,27))
    if int(dia) < 10:
        dia = "0" + dia
    return (dia + "-" + "-".join(fecha))

def convertDate(date): # Date está en formato "month day, year, y lo convierte a formato DD-MMM-AAAA"
    fecha = date.split(" ")
    fecha[1] = fecha[1][0:-1]
    fecha[0] = meses[fecha[0]]
    aux = fecha[1]
    fecha[1] = fecha[0]
    fecha[0] = aux
    fecha = "-".join(fecha)
    return (fecha)

def randomMonth(Q): # Q es Q1 20xx, Q2 20xx.... y así
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    Cuarto = int(Q[1]) ## El numero del cuarto
    numero_Mes = (Cuarto-1)*3
    mes = month[numero_Mes + randint(0,2)]
    dia = str(randint(1,27))
    if int(dia) < 10:
        dia = "0" + dia
    year = Q[3:]
    return (dia + "-" + mes + "-" + year)

#################################################################################################################
#################################################################################################################

# Si las tablas no existen de forma previa, son creadas. En el caso contrario, se omite

def crearTablas(Database):
    cursor = Database.cursor()
    try:
        cursor.execute("CREATE TABLE sansanoplay (id_juego INTEGER NOT NULL, nombre VARCHAR2(80) NOT NULL, precio INTEGER, stock INTEGER, bodega INTEGER, vendidos INTEGER, PRIMARY KEY (id_juego) )")
        print("Se creó la tabla Sansanoplay")
    except:
        print("Error al crear tabla (Quizas ya existe)")
        pass

    try:
        cursor.execute("CREATE TABLE nintendo (id_juego INTEGER NOT NULL, nombre VARCHAR2(120) NOT NULL, genero VARCHAR2(50), desarrollador VARCHAR2(50), publicador VARCHAR2(50), fecha_estreno DATE, exclusividad NUMBER(1), ventas_globales INTEGER, rating INTEGER, PRIMARY KEY (id_juego))")
        print("Se creó la tabla Nintendo")
    except:
        print("Error al crear tabla (Quizas ya existe)")
        pass

#################################################################################################################
#################################################################################################################

def insertSansanoplay(Database, id_juego, nombre, precio, stock, bodega, vendidos):
    try:
        if precio == "":
            precio = str(randint(10,50)*1000-10)
        if stock == "":
            stock = str(randint(1, 100))
        if bodega == "":
            bodega = str(randint(30,100))
        if vendidos == "":
            vendidos = str(randint(100, 6000))

        cursor = Database.cursor()
        cursor.execute("INSERT INTO sansanoplay (id_juego, nombre, precio, stock, bodega, vendidos) VALUES (" + id_juego + ", '" + nombre + "', " + precio + ", " + stock + ", " + bodega + ", " + vendidos + ")")
        return 1
    except:
        return 0

def importSansanoplayCSV(Database):  #Se lee el archivo Sansanoplay.csv

    sansanoplay_CSV = open("Sansanoplay.csv", "r")
    sansanoLines = sansanoplay_CSV.readlines()[1:-1]

    index = 0
    datosInsertados = 0
    while index < len(sansanoLines):

        registroSansano = ""
        id_juego = nombre = precio = stock = bodega = vendidos = ""

        if sansanoLines[index][-2:] == ';\n':
            registroSansano = sansanoLines[index][0:-2]
        else:
            registroSansano = sansanoLines[index][0:-1]

        if registroSansano[0] == '"':
            registroSansano = registroSansano[1:-1]

        listaComandos = []

        if '""' in registroSansano:
            sansanoSplit = registroSansano.split('""')
            sansanoSplit[0] = sansanoSplit[0][1:-1]
            nombre = sansanoSplit[1]

            linea_end = registroSansano.split(",")[-4:]
            id_juego = registroSansano.split(",")[0]
            precio, stock, bodega, precio = linea_end

        else:
            listaComandos = registroSansano.split(",")
            id_juego,nombre,precio,stock,bodega,vendidos = listaComandos

        if "'" in nombre:
            nombre = nombre.split("'")
            nombre = "''".join(nombre)

        datosInsertados += insertSansanoplay(Database, id_juego, nombre, precio, stock, bodega, vendidos)
        index += 1

    if datosInsertados == 0:
        print ("Error en el ingreso. No se ha realizado ningun cambio\nTodos los datos ya están cargados, o se está repitiendo un ID")
    elif datosInsertados == 1:
        print ("Se ha agregado 1 registro a la tabla")
    else:
        print ("Se han agregado " + str(datosInsertados) + " registros a la tabla Sansanoplay")
    cursor = Database.cursor()
    cursor.execute("COMMIT")



def insertNintendo(Database, id_j, nom, gen, dev, pub, rel_date, exc, ven_glob, rat):
        # Se asignan valores aleatorios a los parametros nulos
    try:
        if ven_glob == "":
            ven_glob = str(randint(262143,21478367))
        if rat == "":
            rat = str(randint(4, 10))

        exc = exc.replace("Si", "1")
        exc = exc.replace("No", "0")
        nom = nom.replace("'", "''")
        gen = gen.replace("'", "''")
        dev = dev.replace("'", "''")
        pub = pub.replace("'", "''")
        nom = nom.replace("#", "")
        gen = gen.replace("#", "")
        dev = dev.replace("#", "")
        pub = pub.replace("#", "")


        #print ((id_j, nom, gen, dev, pub, rel_date, exc, ven_glob, rat))

        cursor = Database.cursor()
        cursor.execute("INSERT INTO nintendo (id_juego, nombre, genero, desarrollador, fecha_estreno, publicador, exclusividad, ventas_globales, rating) VALUES (" + id_j + ", '" + nom + "', '" + gen + "', '" + dev + "','" + rel_date + "', '" + pub + "', " + exc + ", " + ven_glob + ", " + rat + ")")

        return 1
    except:
        return 0

def importNintendoCSV(Database):
    nintendo_CSV = open("Nintendo.csv", "r")
    nintendoLines = nintendo_CSV.readlines()[1:-1]

    id_juego = nombre = genero = desarrollador = publicador = fecha_estreno = exclusividad = ventas_globales = rating = ""
    datosInsertados = 0
    index = 0
    while index < len(nintendoLines):
        registroNintendo = nintendoLines[index][0:-11]
        id_juego = nombre = genero = desarrollador = publicador = fecha_estreno = exclusividad = ventas_globales = rating = ""

        if registroNintendo[0] == '"':
            registroNintendo = registroNintendo[1:-1]


        if (("Q1" in registroNintendo) or ("Q2" in registroNintendo) or ("Q3" in registroNintendo) or ("Q4" in registroNintendo)):
            nintendoSplit = registroNintendo.split(",")
            fecha = nintendoSplit[-4]
            nintendoSplit[-4] = randomMonth(fecha)
            id_juego, nombre, genero, desarrollador, publicador, fecha_estreno, exclusividad, ventas_globales, rating = nintendoSplit

        elif ('"' in registroNintendo):     # A continuacion se analiza los casos en que existan nombres separados por comas y ""
            registroNintendo = registroNintendo.split('""')
            registroNintendo[-2] = convertDate(registroNintendo[-2])

            i = 0
            while i < len(registroNintendo):
                registroNintendo[i] = registroNintendo[i].split(",")
                i += 1

            exclusividad, ventas_globales,rating = registroNintendo[-1][1:] # Los ultimos 3 valores pueden obtenerse facilmente, asi que se agregan y se eliminan
            fecha_estreno = registroNintendo[0:-1][-1][0]
            registroNintendo = registroNintendo[0:-2]

            if registroNintendo[0] == registroNintendo[-1]:
                # Este caso se produce cuando al hacer split de "" y obtener la fecha solo queda 1 lista, es decir, ninguna otra parte de la linea contiene ""
                registroSplit = registroNintendo[0]
                id_juego, nombre, genero, desarrollador, publicador = registroSplit[0:-1]

            else:
                for lista in registroNintendo: # Debido al split('""') quedan listas vacias, las cuales se eliminan
                    while '' in lista:
                        lista.remove('')

                id_juego = registroNintendo[0][0] #Se obtiene la ID del juego

                registroNintendo[0].pop(0)
                if registroNintendo[0] == []:
                    registroNintendo.pop(0)
                while [] in registroNintendo:  #Se elimina la ID de la lista, y se revisa que no existan listas vacias
                    registroNintendo.remove([])

                # El resultado es una Lista (L1) de Listas (L2) de Strings.
                # Los distintos elementos de L1 son listas obtenidas de hacer split de "", por lo que son parte del mismo String
                # Elementos de L2 son parametros distintos (como genero, publicador...etc)

                if len(registroNintendo) == 2:
                    nombre = "".join(registroNintendo[0])
                    genero, desarrollador, publicador = registroNintendo[1]
                                #Si la lista tiene len == 2 quiere decir que la lista 1 tiene [nombre] y la lista 2 tiene [genero, desarrollador, publicador]
                else:
                    publicador = registroNintendo[-1][-1] # En el caso contrario, la posicion [-1][-1] siempre corresponde al publicador, por lo que
                                                          # se quita para liberarse de elementos
                    registroNintendo[-1].pop(-1)
                    while [] in registroNintendo:
                        registroNintendo.remove([])       # Se vuelven a eliminar las listas vacias (ocurren por el uso de pop() en una sublista)
                    marcar = False
                    newLista = []       # Se crea un Booleano y una nueva lista vacia (ya se verá por qué)
                    for lista in registroNintendo:
                        if len(lista) == 1:
                            newLista.append(lista)   # Si las listas tiene solo 1 elemento significa que el Nombre está segmentado en distintas listas, y estas son sus partes
                            marcar = True
                                                    # Esto porque contiene "" dentro de su nombre, dividiendose al usar Split. Asi que la linea se "marca", y se añade el
                                                    # segmento a la nueva lista
                    if marcar:
                        for lista in newLista:
                            registroNintendo.remove(lista)
                            nombre += lista[0]
                        genero, desarrollador = registroNintendo[0]     # Si una lista fue marcada, se puede obtener su nombre de unir la nueva lista, y los demás parametros
                                                                        # como el sobrante de la linea
                    else:
                        nombre = registroNintendo[0][0]                 # Si la linea no fue marcada, los parametros pueden obtenerse facilmente
                        registroNintendo[0].pop(0)
                        if len(registroNintendo) == 1:                  # En este caso, el desarrollador es un solo elemento
                            genero, desarrollador = registroNintendo[0]
                        else:
                            genero = registroNintendo[0][0]
                            desarrollador = "".join(registroNintendo[1])    # Y aquí el nombre del desarrollador está segmentado por ",", por lo que se une

        else:
            nintendoSplit = registroNintendo.split(",")
            fecha = nintendoSplit[-4]
            fecha = addDay(fecha)
            nintendoSplit[-4] = fecha
            id_juego, nombre, genero, desarrollador, publicador, fecha_estreno, exclusividad, ventas_globales, rating = nintendoSplit

        datosInsertados += insertNintendo(Database, id_juego, nombre, genero, desarrollador, publicador, fecha_estreno, exclusividad, ventas_globales, rating)
        index +=1

    if datosInsertados == 0:
        print ("Error en el ingreso. No se ha realizado ningun cambio\nTodos los datos ya están cargados, o se está repitiendo un ID")
    elif datosInsertados == 1:
        print ("Se ha agregado 1 registro a la tabla")
    else:
        print ("Se han agregado " + str(datosInsertados) + " registros a la tabla Nintendo")
    cursor = Database.cursor("COMMIT")

#################################################################################################################################
#################################################################################################################################

def inicializarBD(Database):
    crearTablas(Database)
    cursor = Database.cursor()
    importNintendoCSV(Database)
    importSansanoplayCSV(Database)

def deleteTablas(Database):
    cursor = Database.cursor()
    try:
        cursor.execute("DROP TABLE sansanoplay")
        print("Tabla 'Sansanoplay' eliminada")
    except:
        print ("Tabla 'Sansanoplay' no existe")
    try:
        cursor.execute("DROP TABLE nintendo")
        print("Tabla 'Nintendo' eliminada")
    except:
        print ("Tabla 'Nintendo' no existe")


#cursor = Database.cursor()
#deleteTablas(Database)
#crearTablas(Database)
#importSansanoplayCSV(Database)
#importNintendoCSV(Database)

def __main__():

    #cursor = Database.cursor
    #datosConexion = cx_Oracle.makedsn('XenZone489', '1521', service_name='BD213')  # Note
    datosConexion = cx_Oracle.makedsn('localhost', '1521', service_name='BD')      #PC
    Database = cx_Oracle.connect(user='system', password='bd213', dsn=datosConexion) # Datos de admin

    # Para ingresar los datos desde aqui, quitar los comentarios a las siguientes lineas
    # Los datos necesarios están en el directorio de Oracle ->  dbhome/network/admin/tnsnames.ora <<< Abrir con editor de texto e ingresar
    # los datos de la base de datos

    #datosConexion = cx_Oracle.makedsn('Nombre Host', 'Puerto', Service_Name)
    #Database = cx_Oracle.connect(User, Password, dsn=datosConexion)

    """

    datos = input("Ingrese los siguientes datos, separandolos por comas:\n1) Host\n2) Puerto\n3) Service_Name\nIngrese los datos pedidos (host,puerto,S_N): ")
    host, port, service_name = datos.split(",")
    datosConexion = cx_Oracle.makedsn(host, port, service_name)
    datos = input("Haga lo mismo, pero esta vez con su usuario y clave de la base de datos")
    user, passwd = datos.split(",")
    try:
        Database = cx_Oracle.connect(user, passwd, datosConexion)
        print("Conexion exitosa")
    except:
        print("Error de conexion, ingrese denuevo (O edite el archivo '.py' para no ingresar los datos cada vez)")
        ___main___

   """


__main__()