import numpy as np
import pandas as pd
import sqlalchemy as sa

from random import randint as rd
import os




################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

        # Datos para conectarse a la Base de Datos

        # User = Usuario de la Base de Datos
        # Pass = Contraseña de Usuario
        # Db   = SID de la Base de Datos

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

User,Pass,Db = "TestOne","oozei7viing6ooL","Tarea1"

#User, Pass, Db = "system", "bd213", "BD"#213"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
################################################################



Desarrolladores = []
Publicadores = []
Limite_rating = 10


def fixDF2(name2):
    # "Sansanoplay.csv", "Nintendo.csv"
    df2 = pd.read_csv(name2 , sep=',',engine='python')


    ############## edicion Nintendo.csv ##############
    # Q1 2018 -- January 1, 2018 to March 31, 2018
    # Q2 2018 -- April 1, 2018 to June 30, 2018
    # Q3 2018 -- July 1, 2018 to September 30, 2018
    # Q4 2018 -- October 1, 2018 to December 31, 2018


    # Cambio de fechas del database a formato datetime
    df2["fecha de estreno"] = df2["fecha de estreno"].str.replace("Q1","January 1,").str.replace("Q2","April 1,")
    df2["fecha de estreno"] = df2["fecha de estreno"].str.replace("Q3","July 1,").str.replace("Q4","October 1,")
    df2["fecha de estreno"] = pd.to_datetime(df2["fecha de estreno"])


    # ventas globales de cada juego
    df2["ventas globales"] = np.random.randint(0, 5000000, size = len(df2))

    # rating game
    df2["rating"] = np.random.randint(0, Limite_rating + 1, size = len(df2))

    # cambio formato nombres
    df2["nombre"] = df2["nombre"].str.replace(r"\"","'")
    df2["nombre"] = df2["nombre"].astype(str)

    # To str
    # Genero
    df2["genero"] = df2["genero"].astype(str)

    # desarrollador
    df2["desarrollador"] = df2["desarrollador"].astype(str)

    # publicador
    df2["publicador"] = df2["publicador"].astype(str)

    #exclusividad
    df2["exclusividad"] = df2["exclusividad"].str.replace("Si","1").str.replace("No","0")
    df2["exclusividad"] = pd.to_numeric( df2["exclusividad"])

    # nombre columnas
    #id_juego,nombre,genero,desarrollador,publicador,fecha de estreno,exclusividad,ventas globales,rating
    df2.columns = ["id_juego","nombre","genero","desarrollador","publicador","fecha_estreno","exclusividad","ventas_globales","rating"]

    ############## fin edicion nintendo ##############
    return df2





def fixDF1(name1):
    # id_juego,nombre,precio,stock,bodega,vendidos
    df1 = pd.read_csv(name1, sep=',', engine='python')
    ############## inicio edicion sansanoplay.csv ##############
    # cambio formato nombres

    df1["nombre"] = df1["nombre"].str.replace(r"\"","'")
    df1["nombre"] = df1["nombre"].astype(str)

    # precio juegos
    df1["precio"] = np.random.randint(20, 55, size=len(df1))

    # stock juegos
    df1["stock"] = np.random.randint(10, 25, size = len(df1))

    # cantidades en bodega
    df1["bodega"] = np.random.randint(20, 30, size = len(df1))

    # cantidad de juegos vendidos
    df1["vendidos"] = np.random.randint(0, 15, size = len(df1))

     # nombre columnas
    df1.columns = ["id_juego","nombre","precio","stock","bodega","vendidos"]

    ############## fin edicion sansanoplay ##############
    return df1





#--------------------------------------------------------------------------------------------------> main function
#                       CRUD
# nintendo: id_juego,nombre,genero,desarrollador,publicador,fecha de estreno,exclusividad,ventas globales,rating
# sansanoplay: id_juego,nombre,precio,stock,bodega,vendidos

# Importar tablas a SQL


def ToSql(connection):
    # Insertar las tablas en DataBase
    df1 = fixDF1("Sansanoplay.csv")
    df2 = fixDF2("Nintendo.csv")

    try:
        df2.to_sql('nintendo', connection, dtype={'nombre': sa.String(100),
                                              'genero': sa.String(100),
                                              'desarrollador': sa.String(100),
                                              'publicador': sa.String(100)}, index=False)
    except:
        pass

    try:
        df1.to_sql('sansanoplay', connection, dtype={'nombre': sa.String(100)}, index=False)
        return
    except:
        return






# <-------------------- Creacion de vistas ------------------->


# vista de los 5 juegos exclusivos mas caros
def viewTop5(connection):
    connection.execute('''
    CREATE VIEW top_5_exclusive AS
        SELECT *
        FROM(
            SELECT
                sansanoplay.id_juego, sansanoplay.precio,
                sansanoplay.vendidos,
                nintendo.ventas_globales, nintendo.nombre
            FROM
                sansanoplay
            JOIN
                nintendo
            ON
                sansanoplay.id_juego = nintendo.id_juego
            WHERE
                nintendo.exclusividad = 1
            ORDER BY
            sansanoplay.precio DESC
        )
        WHERE
            ROWNUM <=5  ''')
    return connection


# vista de los 3 generos mas vendidos
# if (var = True ) => vista global, else => vista local


def view3Genres(connection, var):
    if var:
    # GLOBAL
        connection.execute('''
        CREATE VIEW top_3_sold_global AS
            SELECT * FROM (
                SELECT genero, CAST(SUM(ventas_globales) AS INTEGER)
                FROM nintendo
                GROUP BY genero
                ORDER BY SUM(ventas_globales) DESC)
            WHERE ROWNUM <=3''')
        return connection
    else:
    # LOCAL
        connection.execute('''
        CREATE VIEW top_3_sold_local AS
            SELECT * FROM(
                SELECT genero, CAST(SUM(vendidos) AS INTEGER) AS sold FROM (
                    SELECT nintendo.id_juego, nintendo.genero, sansanoplay.vendidos
                    FROM nintendo
                    JOIN sansanoplay
                    ON nintendo.id_juego = sansanoplay.id_juego )
                GROUP BY genero
                ORDER BY sold DESC)
            WHERE ROWNUM < 4 ''')
        return connection



# vista de 3 desarrolladores con mas ventas en tienda
def viewDevs(connection):
    connection.execute('''
        CREATE VIEW top_3_dev AS
            SELECT * FROM (
                SELECT desarrollador, CAST(SUM(vendidos) AS INTEGER) AS sold FROM (
                    SELECT nintendo.id_juego, nintendo.desarrollador, sansanoplay.vendidos
                    FROM nintendo
                    JOIN sansanoplay
                    ON nintendo.id_juego = sansanoplay.id_juego)
                GROUP BY desarrollador
                ORDER BY sold DESC)
            WHERE ROWNUM < 4  ''')
    return connection



# vista de juegos por fecha segun rating
def viewRating(connection):
    connection.execute('''
        CREATE VIEW top_rating AS
            SELECT nombre, rating, fecha_estreno
            FROM nintendo where rating = (SELECT rating FROM nintendo ORDER BY rating DESC FETCH FIRST ROW ONLY)
            ORDER BY fecha_estreno DESC
    ''')
    return connection
    # Busca el juego con el rating más alto, y luego busca los juegos con ese mismo rating.



# Eliminar todas las vistas
def dropViews(connection):
    try:
        connection.execute("DROP VIEW top_5_exclusive")
        connection.execute("DROP VIEW top_3_sold_global")
        connection.execute("DROP VIEW top_3_sold_local")
        connection.execute("DROP VIEW top_3_dev")
        connection.execute("DROP VIEW top_rating")
        return
    except:
        return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createViews(connection):    # Crear Vistas

    try:
        viewTop5(connection)            # Top 5 Exclusivos mas caros

        view3Genres(connection, True)   # Top 3 generos mas vendidos (Global)

        view3Genres(connection, False)  # Top 3 generos mas vendidos (Local)

        viewDevs(connection)            # Top 3 Devs con mas ventas locales

        viewRating(connection)          # Juegos con mayor rating

        return
    except:
        return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# <------------------- Fin vistas ------------------------->






# <------------------- Búsqueda --------------------------->

def busqueda(String, connection, bool):

    if bool:
        return connection.execute('''
            SELECT s.id_juego, n.nombre, n.genero, n.rating, n.exclusividad, s.precio, s.stock, s.bodega, s.vendidos
            FROM sansanoplay s
            JOIN nintendo n
            ON s.id_juego = n.id_juego
            WHERE s.id_juego LIKE '%'''+String+'''%'
            ORDER BY s.id_juego
        ''')
    else:
        return connection.execute('''
            SELECT s.id_juego, n.nombre, n.genero, n.rating, n.exclusividad, s.precio, s.stock, s.bodega, s.vendidos
            FROM sansanoplay s
            JOIN nintendo n
            ON s.id_juego = n.id_juego
            WHERE n.nombre LIKE '%'''+String+'''%'
            ORDER BY s.id_juego
        ''')



# <------------------- Eliminación --------------------------->

def deleteRecord(connection, idJuego):
    try:
        connection.execute('''
            DELETE FROM sansanoplay WHERE id_juego = '''+idJuego+'''
        ''')
        print("\nRegistro borrado exitosamente.\n")
    except Exception:
        print("\nError. No se pudo borrar el registro.\nIntente nuevamente.\n")



# <------------------- Insertar --------------------------->


def inputINT(minRange, maxRange):
    try:
        respuesta = int(input("\nSeleccion: "))
        if respuesta > maxRange or respuesta < minRange:
            print("Respuesta invalida")
            return (inputINT(minRange, maxRange))
        else:
            return (respuesta)

    except:
        print("Respuesta invalida")
        return (inputINT(minRange, maxRange))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generos = ["Action", "Action platformer", "Action role-playing", "Action-adventure", "Adventure", "Arcade", "Battle royale", "Beat 'em up",
            "Board game", "Brawler", "Breakout", "Bullet hell", "Card battle", "Card game", "City building", "Collection", "Compilation",
            "Construction", "Construction and management simulation", "Dungeon crawler", "Education", "Educational", "Edutainment",
            "Exergaming", "Exploration", "Fighting", "First-person shooter", "FMV adventure", "Hack and slash", "Hero shooter", "Indie",
            "Interactive fiction", "Japanese role-playing", "Kart racing", "Light gun shooter", "Metroidvania", "Miniature golf",
            "Multiplayer online battle arena", "Music", "Party", "Pinball", "Platform", "Platformer", "Point and click", "Psychological horror",
            "Puzzle", "Puzzle-platformer", "Racing", "Rail shooter", "Real-time strategy", "Rhythm", "Roguelike", "Role-playing", "Sandbox",
            "Shoot 'em up", "Shooter", "Shooting gallery", "Side-scroller", "Simulation", "Space flight simulation", "Sports",
            "Sporting management simulation", "Stealth", "Strategy", "Survival", "Survival horror", "Tactical role-playing", "Tactical shooter",
            "Third-person shooter", "Tower defense", "Turn-based strategy", "Turn-based tactics", "Twin-stick shooter", "Vehicular combat",
            "Vertically scrolling shooter", "Visual novel", "2D shooter", "4X"]



def insertData(connection): #Very long

    os.system('cls')
    print("\n\tInsertar nuevo juego a la base de datos.")
    print("\n\t[1] Insertar SOLO nombre y autorrellenar campos restantes\n\t[2] Insertar varios datos\n\t[3] Cancelar y volver")

    respuesta = inputINT(1,3)   # Se utiliza una funcion que solo permite selecciones entre 1 y 3
    if respuesta == 3:
                                # Si se elige 3, se retorna sin hacer nada
        os.system('cls')
        return

    os.system('cls')

    nombre = ""
    while nombre == "":
        nombre = input("\n\tIngrese nombre del juego: ")    # Se recibe nombre hasta que sea aceptado. (No puede ser nulo)
        if nombre.replace(" ", "") == "":
            print("El nombre no puede estar vacio")
            #Se verifica que no se ingrese un vacio como nombre



    name_search = nombre.lower().replace("-","").replace(" ", "").replace(",", "").replace(".", "").replace("_", "").replace(":", "").replace('"', "").replace("!", "").replace("#", "")
    query = connection.execute("SELECT nombre FROM nintendo").fetchall()

    # Se busca si el nombre ya esta en la base de datos, independiente de capitalizacion.

    for name in query:
        if name[0].lower().replace("-","").replace(" ", "").replace(",", "").replace(".", "").replace("_", "").replace(":", "").replace('"', "").replace("!", "").replace("#","") == name_search:
            print("El juego ya esta en la base de datos. Volviendo")
            return

    # Todos los replace se utilizan para dejar el nombre sin los simbolos especiales marcados, como " , . _ -
    # Es menos eficiente por todos los reemplazos que debe ejecutar, pero busca la mayor compatibilidad posible con nombres ya existentes.
    # Ademas, hay que tener en cuenta que registra toda la base de datos, pues todos los juegos tienen nombres distintos


    nombre = nombre.replace("'", "''") # Se reemplaza en caso de que el nombre tenga apostrofe, por un doble apostrofe (#SQLthings)

    selection = 0

    if respuesta == 2:
        print("\n\tSe pediran los datos para cada campo de los registros.\n\tPuede elegir si responder o dejarlo al azar.")
        print("\tEn caso de ingresar Si en alguna opcion, puede ingresar solo un espacio, y se asignara un valor aleatorio\n")
        print("\n\tIngresar genero?:\n\t\t[1] Si.\n\t\t[2] No.")
        selection = inputINT(1,2)



### Añadir genero

# El procedimiento es similar, pero menos extenso que en el caso anterior, ya que en toda la base de datos hay 78 (mas o menos) generos distintos
# Por lo que resulta más facil buscar en ellos.
# Además, los generos no tienen muchos caracteres especiales, por lo que solo seria necesario revisar el Input, y adecuarlo a un genero preexistente
# cuando sea posible

    genero = ""
    if selection == 1:
        while genero == "":
            genero = input("\n\tIngrese genero del juego: ")   # Se puede anular la insercion manual ingresando un espacio vacio
            if genero == " ":
                print("\n\tSe asignará un genero aleatorio.\n")
                selection = 2
                break
            elif genero.replace(" ", "") == "":  # Fuera del espacio para cancelar, cualquier otra cantidad se considerará vacio e inaceptable
                genero = ""
                print("El genero no puede estar vacio")

        if selection == 1:
            in_lista = False
            for gen in Generos:
                if gen.lower().replace(" ", "").replace("-", "").replace("'", "") == genero.lower().replace(" ", "").replace("-", "").replace("'", ""):
                    genero = gen
                    in_lista = True
                    break   #Si el genero del input se encuentra en la lista, se utiliza ese

            if in_lista == False: # Si el genero ingresado no está en la lista, se estandariza a Primera letra Mayus, y el resto Minus.
                genero = genero[0].lower() + genero[1:].lower()
                Generos.append(genero) #La lista de generos de define fuera de la funcion, para evitar que sea reasignada cada vez, de modo que se puedan ir agregando nuevos generos.

    if selection == 2 or respuesta == 1:
        maxIndex = len(Generos) - 1
        genero = Generos[rd(0, maxIndex)]
    genero = genero.replace("'", "''")
    print("\tSe ha ingresado el genero: "+ genero)



#######################################################################################
# Obtener lista de desarrolladores y publicadores en existencia.
    global Desarrolladores
    global Publicadores
    if len(Desarrolladores) == 0 or len(Publicadores) == 0: #La idea de esto es que se haga solo 1 vez
        Devs = set()
        Pubs = set()

# Se crean sets y se revisan los items de la base de datos. La idea es que no se repitan.
# Se transforman en listas, y se utilizaran luego.

        search = connection.execute("SELECT * FROM nintendo ORDER BY desarrollador").fetchall()
        for dev in search:
            Devs.add(dev[3])
            Pubs.add(dev[4])

# Estos indices son porque la tabla Nintendo esta ordenada de forma:
# 0: ID   ;   1: Nombre   ;   2: Genero   ;   3: Dev   ;   4: Pubs

        Desarrolladores = list(Devs)
        Publicadores = list(Pubs)

######################################################################################

    if respuesta == 2:
        print("\n\tIngresar desarrollador?:\n\t\t[1] Si.\n\t\t[2] No.")
        selection = inputINT(1,2)

    desarrollador = ""

    # Se realiza el mismo procedimiento que en los casos anteriores, ahora recorriendo la base de datos para obtener desarrolladores y
    # publicadores ya existentes. En este caso eran 400+ (creo), asi que, no hay lista...

    if selection == 1:
        while desarrollador == "":
            desarrollador = input("\n\tIngrese desarrollador del juego: ")
            if desarrollador == " ":
                print("\n\tSe asignará un desarrollador aleatorio.\n")
                selection = 2
                break
            elif desarrollador.replace(" ", "") == "":
                desarrollador = ""
                print("El desarrollador no puede estar vacio")

        if selection == 1:
            in_lista = False
            for dev in Desarrolladores:
                if (dev.lower()).replace("-", "").replace(" ", "") == (desarrollador.lower()).replace("-", "").replace(" ", ""):
                    desarrollador = dev
                    in_lista = True
                    break

            if in_lista == False:
                desarrollador = desarrollador[0].upper() + desarrollador[1:].lower()
                Desarrolladores.append(desarrollador)

    if selection == 2 or respuesta == 1:
        randomDev = ["XenTertainment", "Chaldeas", "Yhatoh", "Marcelo Mendoza"]
        maxIndex = len(randomDev) - 1
        desarrollador = randomDev[rd(0, maxIndex)]
    print("\tSe ha ingresado el desarrollador: "+ desarrollador)

####################################
# Añadir publisher
###################################

# Es exactamente lo mismo que en el caso anterior

    if respuesta == 2:
        print("\n\tIngresar publicador?:\n\t\t[1] Si.\n\t\t[2] No.")
        selection = inputINT(1,2)

    publicador = ""

    # Como siempre, Selection 1 es para ingresar de forma manual, y se usa la vieja confiable
    if selection == 1:
        while publicador == "":
            publicador = input("\n\tIngrese publicador del juego: ")
            if publicador == " ":
                print("\n\tSe asignará un publicador aleatorio.\n")
                selection = 2
                break
            elif publicador.replace(" ", "") == "":
                publicador = ""
                print("El publicador no puede estar vacio")

        if selection == 1:
            in_lista = False
            for pub in Publicadores:
                if pub.lower().replace("-", "").replace(" ", "") == publicador.lower().replace("-", "").replace(" ", ""):
                    publicador = pub
                    in_lista = True
                    break

            if in_lista == False:
                publicador = publicador[0].lower() + publicador[1:].lower()
                Publicadores.append(publicador)


    # Esto en caso de que se deje random
    if selection == 2 or respuesta == 1:
        randomPub = ["XenTertainment", "Chaldeas", "Yhatoh", "Marcelo Mendoza"]
        maxIndex = len(randomPub) - 1
        publicador = randomPub[rd(0, maxIndex)]
    print("\tSe ha ingresado el publicador: "+ publicador)

############################################
# Exclusividad:
############################################

# Un simple Si o No. Pero se permite tambien dejarlo al azar

    if respuesta == 2:
        print("\n\tExclusividad del juego:\n\t\t[1] Si.\n\t\t[2] No.\n\t\t[3] Dejar al azar.")
        exclusividad = inputINT(1,3) -1

    if respuesta == 1 or exclusividad == 2:
        exclusividad = rd(0,1)

    if exclusividad == 0:
        print("\tSe definio el juego como Exclusivo")
    else:
        print("\tSe definio el juego como No Exclusivo")


#############################################
# Fecha
############################################

    meses = {"1":"31", "01": "31" , "2": ["28", "29"], "02": ["28", "29"], "3": "31", "03": "31",
             "4": "30", "04": "30", "5": "31", "05": "31", "6": "30", "06": "30",
             "7": "31", "07": "31", "8": "31", "08": "31", "9": "30", "09":"30",
             "10": "31", "11": "30", "12": "31"} # Meses y si cantidad de dias

    fecha = ""
    if respuesta == 2:
        print("\n\tIngresar fecha de lanzamiento?\n\t\t[1] Si.\n\t\t[2] No.")
        selection = inputINT(1,2)

    if selection == 1:
        print ("\n\tIngrese fecha en formato DD/MM/AA")
        while fecha == "":
            inputFecha = input("\tIngrese Fecha: ")

            if inputFecha == " ":
                selection = 2
                break

            opFecha = inputFecha.split("/")
            if len(opFecha) != 3:  # [0] deberia ser DD, [1] MM y [2]: AA
                print("\tFormato de fecha incorrecto")

            else:           # Basicamente muchas condiciones para verificar que la fecha sea valida
                            # Y convertir los numeros a cadenas MM/DD/AA
                            # Porque aunque pida MM o DD, acepta resultados como "1", para darle mas flexibilidad
                try:        # El enorme try catch verifica que lo ingresado pueda ser convertido en INT, y que
                            # cuente con 3 valores separados por "/"

                    limiteDia = 0

                    if opFecha[1] != "02" and opFecha[1] != "2":
                        limiteDia = int(meses[opFecha[1]])
                    else:
                        anno = int(opFecha[2])
                        if (anno % 4 == 0) and (anno % 100 != 0): #bisiesto
                            limiteDia = 29

                        else: # No bisiesto
                            limiteDia = 28

                    if int(opFecha[0]) > 0 and int(opFecha[0]) <= limiteDia: # Se verifica que la fecha sea posible

                        if int(opFecha[1]) < 10:
                            fecha += "0" + str(int(opFecha[1]))
                        else:
                            fecha += opFecha[1]

                        if int(opFecha[0]) < 10:
                            fecha += "/0" + str(int(opFecha[0]))    # Se va convirtiendo el string a uno aceptable
                        else:
                            fecha += "/" + opFecha[0]

                        anno = int(opFecha[2])
                        if anno > 100 or anno < 0:
                            print("\tFecha no permitida")
                            fecha = ""

                        elif anno < 10:
                            anno = "/0" + str(anno)
                            fecha += str(anno)
                        else:
                            fecha += "/" + str(anno)
                            print ("\tSe asigno la fecha " + fecha + " (mostrada como MM/DD/AA)")

                    else:
                        print ("\tLa fecha ingresada no es posible")


                except:
                    fecha = ""   # Si no sirve, se reinicia
                    print ("\tFormato de fecha incorrecto")


    if selection == 2 or respuesta == 1:        # Esto incluye una fecha random, y la convierte en string
                                                # Nada muy raro. Y "limite" es el maximo numero de dias por mes.
                                                # El random usa YY hasta 20, aunque el usuario puede poner hasta 99 si quiere
        anno = rd(0, 20)
        mes = rd(1,12)
        limite = 0
        if mes == 2:
            if (anno % 4 == 0) and (anno % 100 != 0): #Bisiesto
                limite = 29
            else:
                limite = 28
        else:
            limite = int(meses[str(mes)])
        dia = rd(1, limite)

        if dia < 10:
            dia = "0" + str(dia)
        else:
            dia = str(dia)
        if mes < 10:
            mes = "0" + str(mes)
        else:
            mes = str(mes)
        if anno < 10:
            anno = "0" + str(anno)
        else:
            anno = str(anno)

        fecha = mes + "/" + dia + "/" + anno
        print("\tSe asigno la fecha " + fecha)

#######################################################################
# Rating
#######################################################################

    rating = 0      # Bien simple, permite ingresar el rating. Usa una variable global, de modo que el rating maximo
                    # pueda ser cambiado sin afectar el funcionamiento del insert
                    # No permite rating 0, porque... no se, se me ocurrio nomas, 0 me parecio feo
    if respuesta == 2:
        print("\n\tIngresar rating?\n\t\t[1] Si.\n\t\t[2] No.")
        selection = inputINT(1,2)
        if selection == 1:
            while rating == 0:
                Rating = input("Ingrese rating entre 1 y " + str(Limite_rating) + ": ")
                if Rating == " ":
                    selection = 2
                    break
                else:
                    try:
                        Rating = int(Rating)
                        if Rating > 0 and Rating <= Limite_rating:
                            rating = Rating
                            print("\tSe ha ingresado el valor " + str(rating))
                            break
                        else:
                            print("\tEl valor no esta permitido en el rango.")
                    except:
                        print("\tEl valor ingresado no es valido.")

    if respuesta == 1 or selection == 2:
        rating = rd(1,Limite_rating)
        print("\tSe asigno el rating " + str(rating))


#######################################################################
# Nested Function wooooo (Porque esto se hara muchas veces :D)
#######################################################################

    def integerInput(respuesta, string_variable, minRango, maxRango):
        # Retornara el valor a asignar.
        # Respuesta es si se ingresara manualmente o al azar
        # min y max rango los valores posibles entre los que se puede elegir
        # string_variable es lo que se deberia imprimir (como "numero de ventas")

        valor_Final = -1         # Exactamente el mismo funcionamiento que con el rating pero con valores variables
        if respuesta == 2:
            print("\n\tIngresar " + string_variable + "?\n\t\t[1] Si.\n\t\t[2] No.")
            selection = inputINT(1,2)
            if selection == 1:
                while valor_Final == -1:
                    Temporal = input("Ingrese " + string_variable +": ")
                    if Temporal == " ":
                        selection = 2
                        break
                    else:
                        try:
                            Temporal = int(Temporal)
                            if Temporal >= 0:
                                valor_Final = Temporal
                                print("\tSe ha ingresado el valor " + str(valor_Final))
                                return (valor_Final)
                            else:
                                print("\tEl valor no puede ser negativo.")
                        except:
                            print("\tEl valor ingresado no es valido.")

        if respuesta == 1 or selection == 2:
            valor_Final = rd(minRango, maxRango)
            print("\tSe asigno el " + string_variable + " " + str(valor_Final))
            return (valor_Final)

#######################################################################
# El resto
#######################################################################

    ventas_globales = str(integerInput(respuesta, "numero de ventas globales", 0, 5000000))
    precio          = str(integerInput(respuesta, "precio", 2, 60))
    stock           = str(integerInput(respuesta, "stock en tienda", 5, 15))
    bodega          = str(integerInput(respuesta, "stock en bodega", 10, 30))
    ventas_locales  = str(integerInput(respuesta, "numero de ventas locales", 0, 1500))


###################
# Query
###################

    # Se crean variables de 1 letra que contienen una porcion del UPDATE
    # Es lo mismo que colocarlo todo en una sola linea, pero asi es mas "legible"
    # y eso lo digo mas que nada por mi. Eran muchos strings cortos para incluir comillas o comas
    # lo hacia muy horrible de leer

    #############
    # Nintendo:
    #############

    g =   "genero = '"                  + genero             + "', "
    d =   "desarrollador = '"           + desarrollador      + "', "
    p =   "publicador = '"              + publicador         + "', "
    x =   "exclusividad = "             + str(exclusividad)  + ", "
    f =   "fecha_estreno = TO_DATE('"   + fecha              + "', 'MM/DD/YY'), "
    r =   "rating = "                   + str(rating)        + ", "
    vg =  "ventas_globales = "          + ventas_globales

    ################
    # Sansanoplay:
    ################

    pr = "precio = "   + precio   + ", "
    s  = "stock = "    + stock    + ", "
    b  = "bodega = "   + bodega   + ", "
    vl = "vendidos = " + ventas_locales


    connection.execute("INSERT INTO sansanoplay (nombre) VALUES ('" + nombre + "')") # Se inserta el nombre en las tablas
    connection.execute("UPDATE nintendo SET " + g + d + p + x + f + r + vg + " WHERE nombre = '" + nombre + "'") # Se actualiza Nintendo con los datos ingresados
    connection.execute("UPDATE sansanoplay SET " + pr + s + b + vl + " WHERE nombre = '" + nombre + "'") # Se actualiza Sansano
                                        # Tan simple como poner solo iniciales :D


    os.system('cls')
    print("Se han insertado los siguientes valores:\n")

    print ("\tSansanoplay:")
    print (pd.DataFrame(connection.execute("SELECT * FROM sansanoplay WHERE nombre = '" + nombre + "'"), columns = ["id_juego","nombre","precio","stock", "bodega","vendidos"]))

    print ("\n\tNintendo:")
    print (pd.DataFrame(connection.execute("SELECT * FROM nintendo WHERE nombre = '" + nombre + "'"), columns = ["id_juego", "nombre", "genero", "desarrollador",
             "publicador", "fecha_estreno", "exclusividad", "ventas_globales", "rating"]))

    #nintendo: genero, desarrollador, publicador, fecha_estreno, exclusividad, ventas_globales, rating
    #sansanop: precio, stock, bodega, vendidos




# <------------------- Triggers --------------------------->

def createTriggers(connection):

    # Trigger 1: Sincronizar las eliminaciones.
        try:
            connection.execute('''
            CREATE TRIGGER syncDelete AFTER DELETE ON sansanoplay FOR EACH ROW
            BEGIN
                DELETE FROM nintendo WHERE nintendo.id_juego = :OLD.id_juego;
            END;
            ''')
        except:
            pass

    # Trigger 2: Auto_Asignar ID.
        try:
            connection.execute('''
            CREATE TRIGGER auto_ID BEFORE INSERT ON sansanoplay FOR EACH ROW
            BEGIN
                SELECT (MAX(id_juego)+1) INTO :NEW.id_juego FROM sansanoplay;
                INSERT INTO nintendo (id_juego) SELECT (MAX(id_juego)+1) FROM sansanoplay;
            END;
            ''')
        except:
            pass

    # Trigger 3: Sincronizar Insert
        try:
            connection.execute('''
            CREATE TRIGGER syncInsert AFTER INSERT ON sansanoplay
            FOR EACH ROW
            BEGIN
                UPDATE nintendo SET nombre = :NEW.nombre WHERE id_juego = :NEW.id_juego;
            END;
            ''')
            return
        except:
            return


def dropTriggers(connection):

    # Eliminacion Trigger 1.
        try:
            connection.execute("DROP TRIGGER syncDelete")
        except:
            pass

    #Eliminacion Trigger 2:
        try:
            connection.execute("DROP TRIGGER auto_ID")
        except:
            pass

    #Eliminacion Trigger 3
        try:
            connection.execute("DROP TRIGGER syncInsert")
            return
        except:
            return


# <------------------- Triggers --------------------------->






# <------------------- Tablas --------------------------->

def dropTables(connection):
    try:
        connection.execute("DROP TABLE NINTENDO")
        connection.execute("DROP TABLE SANSANOPLAY")
        return
    except:
        print ("Ocurrio un problema, no se pudieron eliminar las tablas")
        return



# <------------------- Tablas --------------------------->



# <------------------- Venta --------------------------->
def Sell(connection, idJuego, unitsSold):
    stock = connection.execute(
            '''SELECT stock FROM sansanoplay WHERE id_juego = '''
            + idJuego).fetchall()[0][0]

    if int(unitsSold) < stock and int(unitsSold) > 0:
        connection.execute('''
            UPDATE
                nintendo
            SET
                ventas_globales = ventas_globales + '''+unitsSold+'''
            WHERE
                id_juego = '''+idJuego+'''
        ''')
        connection.execute('''
            UPDATE
                sansanoplay
            SET
                vendidos = vendidos + '''+unitsSold+''',
                stock = stock - '''+unitsSold+'''
            WHERE
                id_juego = '''+idJuego+'''
        ''')
        return True
    else:
        print("\nNo es posible realizar la venta.\n")
        return False

def verifyStock(tabla, connection, idJuego):

    stock = connection.execute(
            sa.select(
                [tabla.c.stock]
            ).where(
            tabla.c.id_juego == int(idJuego))).fetchall()[0][0]
    bodega = connection.execute(
            sa.select(
                [tabla.c.bodega]
            ).where(
            tabla.c.id_juego == int(idJuego))).fetchall()[0][0]

    if stock < 10 :
        print("\nTienda:\tSIN STOCK\n")
        print("\n\t\t[VERIFICAR BODEGA]")

        if bodega > 0:
            print("\nBodega:\t",bodega)
            print("\n\t\t[REPONER STOCK 10]")

            connection.execute('''
            update
                sansanoplay
            set
                stock = stock + 10,
                bodega = bodega - 10
            where
                id_juego = '''+idJuego+'''
            ''')
            print("\n\t\t[STOCK ACTUALIZADO]\n")
            return True
        else:
            print("\nBodega:\tSIN STOCK\n")
            print("\nNO SE HA PODIDO ACTUALIZAR STOCK")
            return False
    else:
        print("\nQuedan ",stock," unidades.\n")
        return True




def __main__():

    try:
        oracle_db = sa.create_engine('oracle://'+User+':'+Pass+'@'+Db)
        connection = oracle_db.connect()

    except:
        print("No se ha podido conectar. Por favor revise los datos de la conexion.")
        exit()

##############################################################

    ToSql(connection) # Crear Tablas

    createTriggers(connection) # Crear Triggers

    createViews(connection) #Crear Vistas

##############################################################

    # Metadata de las tablas de la Base de Datos
    metadata = sa.MetaData(bind=connection)

    # Tablas de la Base de Datos
    nintendo    = sa.Table('nintendo',    metadata, autoload=True, autoload_with=oracle_db)
    sansanoplay = sa.Table('sansanoplay', metadata, autoload=True, autoload_with=oracle_db)


    # Vistas de la Base de Datos segun especificaciones de la tarea
    top5  = sa.Table('top_5_exclusive',   metadata, autoload=True, autoload_with=oracle_db)
    top3G = sa.Table('top_3_sold_global', metadata, autoload=True, autoload_with=oracle_db)
    top3L = sa.Table('top_3_sold_local',  metadata, autoload=True, autoload_with=oracle_db)
    top3D = sa.Table('top_3_dev',         metadata, autoload=True, autoload_with=oracle_db)
    topR  = sa.Table('top_rating',        metadata, autoload=True, autoload_with=oracle_db)


    V1 = connection.execute(sa.sql.select([top5])).fetchall()
    V2 = connection.execute(sa.sql.select([top3G])).fetchall()
    V3 = connection.execute(sa.sql.select([top3L])).fetchall()
    V4 = connection.execute(sa.sql.select([top3D])).fetchall()
    V5 = connection.execute(sa.sql.select([topR])).fetchall()


    # Ejemplo select x from t where clause
    #stmt = sa.select([nintendo.c.id_juego,nintendo.c.nombre]).where(nintendo.c.id_juego == 1)
    #print(connection.excecute(stmt))




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     MENU PRINICIPAL     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


    while 1:
        print("\nQue desea hacer?:\n\n\tOpciones de Vista:\n\t  [1] Top 5 juegos exclusivos mas caros.")
        print("\t  [2] Top 3 géneros más vendidos globalmente.\n\t  [3] Top 3 géneros más vendidos localmente.")
        print("\t  [4] Top 3 desarrolladoras con más ventas locales.\n\t  [5] Juegos con el mayor rating.")
        print("\n\tOpciones CRUD:\n\t  [6] Buscar un juego.\n\t  [7] Eliminar un juego (Por favor verificar elminación buscando el juego).")
        print("\t  [8] Vender juego.\n\t  [9] Insertar nuevo juego.")
        print("\n\tOpciones de Salida:\n\t  [-100] Salir y guardar cambios.\n\t  [-101] Salir y eliminar datos.")


        while True:
            try:
                option = int(input("\nSelección: "))
                break
            except ValueError:

                os.system('cls')
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("\n\tOops! Respuesta no válida. Por favor ingrése número nuevamente...\n")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("\nQue desea hacer?:\n\n\tOpciones de Vista:\n\t  [1] Top 5 juegos exclusivos mas caros.")
                print("\t  [2] Top 3 géneros más vendidos globalmente.\n\t  [3] Top 3 géneros más vendidos localmente.")
                print("\t  [4] Top 3 desarrolladoras con más ventas locales.\n\t  [5] Juegos con el mayor rating.")
                print("\n\tOpciones CRUD:\n\t  [6] Buscar un juego.\n\t  [7] Eliminar un juego (Por favor verificar elminación buscando el juego).")
                print("\t  [8] Vender juego.\n\t  [9] Insertar nuevo juego.")
                print("\n\tOpciones de Salida:\n\t  [-100] Salir y guardar cambios.\n\t  [-101] Salir y eliminar datos.")




        if option == 1:
            os.system('cls')
            print("\n\n<---------------- TOP 5 EXCLUSIVOS MAS CAROS --------------------------->\n")
            print(pd.DataFrame(V1,columns=["GAME_ID","PRICE (USD)","SOLD","GLOBAL SALES", "NAME"]))
            print("\n\n")


        elif option == 2:
            os.system('cls')
            print("\n\n<--------- TOP 3 GENEROS MAS VENDIDOS GLOBALMENTE ------------->\n")
            print(pd.DataFrame(V2, columns = ["GENRE", "SALES"]))
            print("\n\n")


        elif option == 3:
            os.system('cls')
            print("\n\n<-------------- TOP 3 GENEROS MAS VENDIDOS LOCALMENTE ------------------->\n")
            print(pd.DataFrame(V3, columns = ["GENRE", "SALES"]))
            print("\n\n")


        elif option == 4:
            os.system('cls')
            print("\n\n<------ TOP 3 DESARROLLADORES CON MAS VENTAS ------>\n")
            print(pd.DataFrame(V4, columns = ["DEVELOPER", "SALES"]))
            print("\n\n")


        elif option == 5:
            os.system('cls')
            print("\n\n<-------------- TOP RATINGS ------------------->\n")
            print(pd.DataFrame(V5, columns = ["NAME", "RATING", "RELEASE DATE"]).to_string())
            print("\n\n")


        elif option == 6:
            print("Desea realizar búsqueda por ID o por nombre del juego?\n\n[1] ID\n[2] Nombre")
            while True:
                try:
                    tp = int(input("\nSelección: "))
                    if tp == 1 or tp == 2:
                        break
                    else:
                        print("Valor incorrecto. Ingrese selección nuevamente.")

                except ValueError:
                    print("Oops! Valor no válido. Por favor ingrése número nuevamente...")

            string = input("\nIngrese búsqueda: ")

            if tp == 1:
                query = busqueda(string, connection, True)
            elif tp == 2:
                query = busqueda(string, connection, False)

            newDat = pd.DataFrame(query, columns = ["id_juego","nombre","genero","rating",
                                                    "exclusividad","precio","stock","bodega","vendidos"])
            os.system('cls')

            if not newDat.empty:
                print("Resultados Búsqueda\n")
                print(newDat)
            else:
                print("Búsqueda sin resultados.")
            print("\n\n")



        elif option == 7:
            string = input("\nIngrese registro a borrar (ID_JUEGO): ")
            deleteRecord(connection, string)



        elif option == 8:

            idGame = input("\nIngrese ID del juego a vender: ")
            if not pd.DataFrame(busqueda(idGame, connection, True)).empty:
                if verifyStock(sansanoplay, connection, idGame):

                    try:
                        quantity = input("Ingrese cantidades a vender: ")
                        if Sell(connection, idGame, quantity):
                            print("\nVenta realizada exitosamente.\n")
                        else:
                            print("\nNo hay stock ni en tienda ni en bodega, llame a su jefe.")

                    except ValueError:
                        print("Oops! Valor no válido. Por favor ingrése número nuevamente...")

            else:
                print("\nID inválido.\n")


        elif option == 9:
            insertData(connection)

        elif option == 20:
            print("TEST")
            print(connection.execute("SELECT * FROM nintendo WHERE id_juego = 1400").fetchall())


        elif option == -100:
            os.system('cls')
            exit()

        elif option == -101:
            os.system('cls')
            dropTables(connection)
            dropViews(connection)
            dropTriggers(connection)
            exit()

        else:
            os.system('cls')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("\n\tOpción no válida.\n")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


__main__()