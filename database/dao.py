from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_albums(d):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select a.id as id, a.title as title, (sum(t.milliseconds)/60000) as duration
                from album a, track t
                where a.id = t.album_id 
                group by a.id, a.title
                having (sum(t.milliseconds)/60000) > %s
        """

        cursor.execute(query, (d,))

        for row in cursor:
            album = Album(row['id'], row['title'], row['duration'])
            result.append(album)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_connections(dict_albums):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select distinct atp1.a_id as a1, atp2.a_id as a2
                    from (select t.id as t_id, a.id as a_id, pt.playlist_id as p_id
                    from album a, track t, playlist_track pt 
                    where a.id = t.album_id and t.id = pt.track_id ) as atp1,
                    (select t.id as t_id, a.id as a_id, pt.playlist_id as p_id
                    from album a, track t, playlist_track pt 
                    where a.id = t.album_id and t.id = pt.track_id ) as atp2,
                    playlist_track pt
                    where pt.playlist_id = atp1.p_id and pt.playlist_id = atp2.p_id and 
                    atp1.a_id > atp2.a_id
            """

        cursor.execute(query)

        for row in cursor:
            connection = (dict_albums[row['a1']], dict_albums[row['a2']])
            result.append(connection)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_playlist_map(albums, dict_albums):
        conn = DBConnect.get_connection()

        result = {a: set() for a in albums}
        album_ids = tuple(a.id for a in albums)
        if not album_ids:
            return result

        cursor = conn.cursor(dictionary=True)
        query = f"""
                select t.album_id as a_id, pt.playlist_id as p_id
                from track t, playlist_track pt 
                where t.id = pt.track_id and t.album_id in {album_ids}
                """

        cursor.execute(query)

        for row in cursor:
            album = dict_albums[row['a_id']]
            result[album].add(row['p_id'])

        cursor.close()
        conn.close()
        return result