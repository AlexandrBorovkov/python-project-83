from psycopg2.errors import UniqueViolation
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS urls (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(255) UNIQUE NOT NULL,
                created_at DATE DEFAULT CURRENT_DATE
                )""")
        self.conn.commit()

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save(self, url):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """INSERT INTO urls (name) VALUES
                    (%s) RETURNING id""",
                    (url["url"],)
                )
                id = cur.fetchone()[0]
                url['id'] = id
                self.conn.commit()
                return True
            except UniqueViolation:
                self.conn.rollback()
                return
