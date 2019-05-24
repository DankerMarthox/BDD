import numpy as np
import pandas as pd
import sqlalchemy as sa

from random import randint as rd
import os


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
    df1 = pd.read_csv(name1 , sep=',', engine='python')
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

    df2.to_sql('nintendo', connection, dtype={'nombre': sa.String(100), 
                                              'genero': sa.String(100),
                                              'desarrollador': sa.String(100),
                                              'publicador': sa.String(100)}, 
                if_exists='replace', index=False)
    df1.to_sql('sansanoplay', connection, dtype={'nombre': sa.String(100)}, 
                if_exists='replace', index=False)

    return connection


# <-------------------- Creacion de vistas ------------------->

# vista de los 5 juegos exclusivos mas caros
def viewTop5(connection):
    connection.execute('''
    create view TOP_5_EXCLUSIVE AS
        select *
        from(
            select 
                sansanoplay.id_juego,sansanoplay.precio,
                sansanoplay.vendidos,
                nintendo.ventas_globales, nintendo.nombre 
            from 
                sansanoplay 
            join 
                nintendo 
            on 
                sansanoplay.id_juego = nintendo.id_juego 
            where
                nintendo.exclusividad = 1
            order by 
            sansanoplay.precio desc
        )
        where
            rownum <=5  ''')


# vista de los 3 generos mas vendidos 
# if (var = True ) => vista global, else => vista local
def view3Genres(connection, var):
    if var:
        # GLOBAL
        connection.execute('''
        create view TOP_3_SOLD_GLOBAL AS
            select * from (
                select genero, sum(ventas_globales)
                from nintendo 
                group by genero 
                order by sum(ventas_globales) desc)
            where rownum <=3''')
    else:
        # LOCAL
        connection.execute('''
        create view TOP_3_SOLD_LOCAL as
            select * from(
                select genero, sum(vendidos) as sold from (
                    select nintendo.id_juego, nintendo.genero, sansanoplay.vendidos
                    from nintendo
                    join sansanoplay
                    on nintendo.id_juego = sansanoplay.id_juego )
                group by genero
                order by sold desc)
            where rownum <= 3 ''')

# Eliminar todas las vistas
def dropViews(connection):
    connection.execute("drop view TOP_5_EXCLUSIVE")
    connection.execute("drop view TOP_3_SOLD_GLOBAL")
    connection.execute("drop view TOP_3_SOLD_LOCAL")


# <------------------- Fin vistas ------------------------->

# <------------------- Búsqueda --------------------------->

def busqueda(String, connection):

    return connection.execute('''

        select s.id_juego, n.nombre,n.genero,n.rating,n.exclusividad,
               s.precio,s.stock,s.bodega,s.vendidos
        from sansanoplay s
        join nintendo n
        on s.id_juego = n.id_juego
        where (n.nombre like '%'''+String+'''%')
        or (s.id_juego like '%'''+String+'''%')
        order by s.id_juego
    ''')

# <------------------- Eliminación --------------------------->

def deleteRecord(connection, id):
    try:
        connection.execute('''
            delete from sansanoplay where id_juego = '''+id+'''
        ''')
        connection.execute('''
            delete from nintendo where id_juego = '''+id+'''
        ''')
    except Exception:
        print("Error. No se pudo borrar el registro.\nIntente nuevamente.")


def __main__():

    User,Pass,Db = "TestOne","oozei7viing6ooL","Tarea1"
    oracle_db = sa.create_engine('oracle://'+User+':'+Pass+'@'+Db)
    connection = oracle_db.connect()

    # ToSql(connection)
    # dropViews(connection)
    # viewTop5(connection)
    # view3Genres(connection, True)
    # view3Genres(connection, False)
    
    # Metadata de las tablas del database
    metadata = sa.MetaData(bind=connection)

    # Tablas del database
    nintendo = sa.Table('nintendo', metadata, autoload=True, autoload_with=oracle_db)
    sansanoplay = sa.Table('sansanoplay', metadata, autoload=True, autoload_with=oracle_db)

    # Views del Database segun especificaciones de la tarea
    top5 = sa.Table('TOP_5_EXCLUSIVE', metadata, autoload=True, autoload_with=oracle_db)
    top3G = sa.Table('TOP_3_SOLD_GLOBAL', metadata, autoload=True, autoload_with=oracle_db)
    top3L = sa.Table('TOP_3_SOLD_LOCAL', metadata, autoload=True, autoload_with=oracle_db)

    
    V1 = connection.execute(sa.sql.select([top5])).fetchall()
    V2 = connection.execute(sa.sql.select([top3G])).fetchall()
    V3 = connection.execute(sa.sql.select([top3L])).fetchall()

    # Ejemplo select x from t where clause
    #stmt = sa.select([nintendo.c.id_juego,nintendo.c.nombre]).where(nintendo.c.id_juego == 1)
    #print(connection.excecute(stmt))
    while 1:
        print("Que desea ver?:\n\n\t[1] Top 5 juegos exclusivos mas vendidos.")
        print("\t[2] Top 3 géneros más vendidos globalmente.\n\t[3] Top 3 géneros más vendidos localmente.")
        print("\t[4] Buscar un juego.\n\t[5] Eliminar un juego (Por favor verificar elminación buscando el juego).")        
        print("\t[-100] Exit.")

        while True:
            try:
                option = int(input("\nSelección: "))
                break
            except ValueError:
                print("Oops! Número no válido. Por favor ingrése número nuevamente...")
        if option == 1:
            os.system('cls')
            print("\n\n<-------------- TOP JUEGOS EXCLUSIVOS MAS CAROS ------------------------->\n")    
            print(pd.DataFrame(V1,columns=["GAME_ID","PRICE (USD)","SOLD","GLOBAL SALES", "NAME"]))
            print("\n\n")

        elif option == 2:
            os.system('cls')
            print("\n\n<-------------- TOP 3 GENEROS MAS VENDIDOS GLOBALMENTE ------------------>\n")
            print(pd.DataFrame(V2, columns = ["GENRE", "SALES"]))
            print("\n\n")

        elif option == 3:
            os.system('cls')
            print("\n\n<-------------- TOP 3 GENEROS MAS VENDIDOS LOCALMENTE ------------------->\n")
            print(pd.DataFrame(V3, columns = ["GENRE", "SALES"]))
            print("\n\n")
        
        elif option == 4:
            string = input("\nIngrese búsqueda: ")
            query = busqueda(string, connection)
            os.system('cls')
            print(pd.DataFrame(query, columns = ["id_juego","nombre","genero","rating",
                                                "exclusividad","precio","stock","bodega","vendidos"]))
            print("\n\n")

        elif option == -100:
            break


__main__()