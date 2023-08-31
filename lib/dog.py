import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.execute("SELECT last_insert_rowid()").fetchone()[0]
        else:
            sql = """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)  # Create a new instance
        dog.save()  # Save it to the database
        return dog  # Return the new instance
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])  # Create a new instance with data from the row
        dog.id = row[0]  # Set the id attribute from the row
        return dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None
        

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name_and_breed(name, breed)
        if existing_dog:
            return existing_dog
        else:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (name, breed))
            CONN.commit()
            new_dog_id = CURSOR.lastrowid
            return cls.find_by_id(new_dog_id)
        

    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ?"
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None
        

    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
