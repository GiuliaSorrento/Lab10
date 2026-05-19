from database.DB_connect import DBConnect
from model.arcoConfine import ArcoConfine
from model.country import Country
class DAO():
    def __init__(self):
        pass

    #i vertici sono tutte le nazioni tra le quali esiste un confine in un anno specificato
    #gli archi (non orientati e non pesati) rappresentano i confini via terra (conttype=1)
    @staticmethod
    def getAllNodes(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []  #lista di nazioni
        # Selezioniamo i campi di country e usiamo alias coerenti con la tua dataclass Country

        #UNION: crea un grande elenco di tutti gli statiID sia nella colonna 1 che nella 2 che compaiono fino all'anno 2000
        #in getAllNodes non devi specificare i confini di terra, devi prendere tutti gli stati che hanno confini in quegli anni
        #se sono presenti o nella colonna 1 o nella 2 avranno sicuramente almeno un confine
        query = """SELECT c.StateAbb AS StateAbb, c.CCode AS CCode, c.StateNme AS StateNme
                   FROM country c
                   WHERE c.CCode IN (
                       SELECT state1no FROM contiguity WHERE year <= %s
                       UNION
                       SELECT state2no FROM contiguity WHERE year <= %s
                   )"""

        cursor.execute(query,(anno,anno,))
        # unpack si può fare quando ti selezioni tutti gli attributi e ti crei l'oggetto intero
        for row in cursor:
            res.append(
                Country(**row))  # (**row) UNPACK significa:  res.append(ArtObject(object_id=row["object_id], ....)

        cursor.close()
        conn.close()
        return res

    # gli archi (non orientati e non pesati) rappresentano i confini via terra (conttype=1)
    @staticmethod
    def getAllEdges(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []  # lista di archiConfine
        #unisci con un arco solo gli stati che hanno un confine di terra
        #fino all'annp indicato
        #la diseguaglianza serve per evitare doppioni visto che
        #possiamo avere due coppie uguali ma invertite
        #tu devi fare un solo arco per ogni coppia
        query ="""SELECT state1no AS nazione1, state2no AS nazione2, year AS anno
                   FROM contiguity 
                   WHERE conttype = 1 
                     AND year <= %s 
                     AND state1no < state2no
                 """

        cursor.execute(query, (anno,))
        # unpack si può fare quando ti selezioni tutti gli attributi e ti crei l'oggetto intero
        for row in cursor:
            res.append(
                ArcoConfine(**row))  # (**row) UNPACK significa:  res.append(ArtObject(object_id=row["object_id], ....)

        cursor.close()
        conn.close()
        return res
