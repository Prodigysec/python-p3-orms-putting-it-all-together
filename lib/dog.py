import sqlite3

CONN = sqlite3.connect("lib/dogs.db")
CURSOR = CONN.cursor()


class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(self):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)


    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)

        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (name, breed))

        # dog.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        dog.id = CURSOR.lastrowid

        return dog

    @classmethod
    def new_from_db(cls, row):
        song = cls(row[1], row[2])
        song.id = row[0]
        return song

    # @classmethod
    # def new_from_db(cls, row):
    #     song = cls(row[1], row[2])
    #     song.id = row[0]
    #     return song

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)


    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            AND breed = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,breed)).fetchone()

        if dog == None:
            dog = cls(name, breed)
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (name, breed))
            # dog.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
            dog.id = CURSOR.lastrowid
            return dog


    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))


    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))



    def save(self):
        dog = Dog(self.name, self.breed)
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        dog.id = CURSOR.lastrowid
        print(f"result => {(dog.id, dog.name, dog.breed)}")

        return (dog.id, dog.name, dog.breed)
