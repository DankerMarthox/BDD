import numpy as np
import pandas as pd
import sqlalchemy as sa

from random import randint as rd


def fixDF2(name2):
    # "Sansanoplay.csv", "Nintendo.csv"
    df2 = pd.read_csv(name2 , sep=',',engine='python')

    ############## edicion Nintrendo.csv ##############
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
    df2["rating"] = np.random.randint(0, 5, size = len(df2))

    # cambio formato nombres
    df2["nombre"] = df2["nombre"].str.replace(r"\"","'")

    #exclusividad
    df2["exclusividad"] = df2["exclusividad"].str.replace("Si","1").str.replace("No","0")

    # nombre columnas 
    #id_juego,nombre,genero,desarrollador,publicador,fecha de estreno,exclusividad,ventas globales,rating
    df2.columns = ["id_juego","nombre","genero","desarrollador","publicador","fecha_estreno","exclusividad","ventas_globales","rating"]

    ############## fin edicion nintendo ##############
    return df2

def fixDF1(name1):
    # id_juego,nombre,precio,stock,bodega,vendidos
    df1 = pd.read_csv(name1 , sep=',', engine='python')
    ############## inicio edicion sansanoplay.csv ##############
   
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

#--------------------------------------------------------------------------------------------------> main functions
def connectToDatabase(Name, port, serviceName, user, pwd):
    con = cx.makedsn(Name, port, service_name = serviceName)
    Dat = cx.connect(user = user, password = pwd, dsn = con)
    return Dat


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


def __main__():

    oracle_db = sa.create_engine('oracle://TestOne:oozei7viing6ooL@Tarea1')
    connection = oracle_db.connect()
    
    df1 = fixDF1("Sansanoplay.csv")
    df2 = fixDF2("Nintendo.csv")
    
    df1.to_sql('sansanoplay', connection, if_exists='replace', index=False)
    df2.to_sql('nintendo', connection, if_exists='replace', index=False)


    #crearTablas(DB)
    #insertCSVToDat(df1, DB, "sansanoplay" )


__main__()