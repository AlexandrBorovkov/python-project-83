import psycopg2
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""SELECT
                                urls.id,
                                urls.name,
                                url_checks.status_code,
                                MAX(url_checks.created_at) as created_at
                            FROM urls
                            LEFT join url_checks on urls.id = url_checks.url_id
                            GROUP by urls.id, urls.name, url_checks.status_code
                            ORDER BY urls.id DESC;""")
                return [dict(row) for row in cur]

    def find_by_id(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def find_by_name(self, name):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
                row = cur.fetchone()
                return dict(row) if row else None

    def save_url(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO urls (name) VALUES
                    (%s) RETURNING id""",
                    (url["url"],)
                )
                id = cur.fetchone()[0]
                url['id'] = id
                conn.commit()

    def save_check(self, data):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO url_checks
                    (url_id, status_code, h1, title, description)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    (
                        data["url_id"],
                        data["status_code"],
                        data["h1"],
                        data["title"],
                        data["description"],
                    )
                )
                conn.commit()

    def get_checks(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    """SELECT * FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC""",
                    (int(url_id),)
                    )
                return [dict(row) for row in cur]
