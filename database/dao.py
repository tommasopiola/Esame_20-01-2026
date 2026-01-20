from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_selez(soglia):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT al.artist_id as id_artist
                FROM artist ar, album al 
                WHERE al.artist_id = ar.id
                GROUP BY id_artist
                HAVING COUNT(*) >= %s
                    
                """
        cursor.execute(query, (soglia,))
        for row in cursor:
            result.append(row['id_artist'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artist_collegati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select a1.artist_id as artista1, a2.artist_id as artista2, COUNT(distinct t1.genre_id) as peso
                    from album a1, track t1, album a2, track t2
                    where a1.id = t1.album_id
                    and a1.artist_id != a2.artist_id
                    and a2.id = t2.album_id
                    and t1.genre_id = t2.genre_id
                    group by artista1, artista2
                """
        cursor.execute(query)
        for row in cursor:
            result.append((row['artista1'], row['artista2'], row['peso']))
        cursor.close()
        conn.close()
        return result
