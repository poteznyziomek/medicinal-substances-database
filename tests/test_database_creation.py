import unittest
import os, os.path
import substances.database as db
import sqlite3


class ExistenceAndBadValues(unittest.TestCase):

	def setUp(self):
		"""Create database and connect to it."""
		db.create_db()
		if os.path.exists("substances.db"):
			self.con = sqlite3.connect("substances.db")
			self.cur = self.con.cursor()
		else:
			raise Exception("Failed to connect, substances.db does not exist.")
	
	def tearDown(self):
		"""Close connection to db and remove its file."""
		self.con.close()
		current_directory = os.getcwd()
		(head, tail) = os.path.split(current_directory)
		#print(f"\nbefore the if\n{head=} {tail=}")
		if tail == "tests":
			os.chdir("..")
			(head, tail) = os.path.split(current_directory)
			#print("Inside the if:")
			#print(f"{head=} {tail=}")
		#print("after the if")
		#print(f"substances.db exists: {os.path.exists("substances.db")}")
		if os.path.exists("substances.db"):
			os.unlink("substances.db")
		else:
			raise Exception(f"no file named 'substances.db' inside {tail}")
	
	def test_fetch_from_nonexistent_table(self):
		"""Raise OperationalError when fetching from nonexistent table."""
		query = """
			SELECT *
			FROM Hunters;
		"""
		self.assertRaises(sqlite3.OperationalError, self.con.execute, query)
	
	def test_Leki_primary_key_null(self):
		"""Primary key bloz cannot be NULL."""
		query1 = """
			INSERT INTO Leki(bloz)
			VALUES (NULL);
		"""
		query2 = """
			INSERT INTO Leki(nazwaHandlowa, postac)
			VALUES ('Bungee gum', 'bungee and gum');
		"""
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query1)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query2)
	
	def test_Producenci_primary_key_null(self):
		"""Primary key {producent, siedziba} cannot be NULL."""
		query1 = """
			INSERT INTO Producenci(producent, siedziba)
			VALUES ('Killua Zoldyck', NULL);
		"""
		query2 = """
			INSERT INTO Producenci(producent, siedziba)
			VALUES (NULL, 'Zoldyck Family');
		"""
		query3 = """
			INSERT INTO Producenci(prezes, rokZalozenia)
			VALUES ('Silva Zoldyck', 2025);
		"""
		query4 = """
			INSERT INTO Producenci(producent, prezes)
			VALUES ('Phantom Troupe', 'Chrollo Lucifer');
		"""
		query5 = """
			INSERT INTO Producenci(siedziba, prezes, rokZalozenia)
			VALUES ('Hunter Association', 'Isaac Netero', 2025);
		"""
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query1)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query2)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query3)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query4)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query5)
	
	def test_Leki_primary_key_not_unique_values(self):
		"""Inserting tuples with equal key value should raise IntegrityError."""
		query = """
			INSERT INTO Leki
			VALUES (1234567, 'Gon', 'Zetsu', 'Concealment', 0.1, 'Nie', 'Various', 'Hunters', 'Whale Island'),
			(1234567, 'Zushi', 'Ren', 'Enhancement', 0.33, 'Tak', 'Multiple', 'Spiders', 'Heavens Arena');
		"""
		self.assertRaises(sqlite3.IntegrityError, self.cur.execute, query)
	
	def test_Producenci_primary_key_not_unique_values(self):
		"""Inserting tuples with equal key value should raise IntegrityError."""
		query = """
			INSERT INTO Producenci
			VALUES ('Uvogin', 'undisclosed', 'Chrollo', 2024),
			('Uvogin', 'undisclosed', 'Hisoka', 2011);
		"""
		self.assertRaises(sqlite3.IntegrityError, self.cur.execute, query)
	
	def test_Leki_UNIQUE_keys(self):
		"""Insereting tuples with equal UNIQUE value(s) should raise IntegrityError."""
		query1 = """
			INSERT INTO Leki(bloz, nazwaHandlowa)
			VALUES (123756, 'Ten'), (321567, 'Ten');
		"""
		query2 = """
			INSERT INTO Leki(bloz, substancjaAktywna, postac, dawka)
			VALUES (321765, 'Ren', 'Aura', 0.0001), (567321, 'Ren', 'Aura', 0.0001);
		"""
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query1)
		self.assertRaises(sqlite3.IntegrityError,
						 self.cur.execute, query2)
	
	def test_FOREIGN_KEY_producent_siedziba_integrity(self):
		"""Raise IntegrityError when inserting into Leki without corresponding tuple in Producenci."""
		query = """
			INSERT INTO Leki(bloz, siedziba, producent)
			VALUES (1324657, 'York New City', 'The Mob');
		"""
		self.con.execute("PRAGMA foreign_keys=1")
		self.cur.execute(query)
		self.assertRaises(sqlite3.IntegrityError, self.con.commit)
	
	def test_Leki_CHECK_bloz_seven_digits(self):
		"""bloz should be seven digits long."""
		query_template = "INSERT INTO Leki(bloz) VALUES ({});"
		incorrect_bloz_values = [
			1, 2, 3, 4, 5, 13, 23, 37, 547, 701,1087,
			1427, 2222, 10867, 100057, 111111, 593933,
			10000000, 12345678, 123456789, 482071529
		]
		for number in incorrect_bloz_values:
			self.assertRaises(
				sqlite3.IntegrityError,
				self.cur.execute,
				query_template.format(number))
	
	def test_Leki_OTC_CHECK_allowed_values(self):
		"""OTC is one of {Tak, Nie, Rpw}."""
		query_template = "INSERT INTO Leki(bloz, OTC) VALUES (1726354, '{}');"
		incorrect_OTC_values = [
			"Nen", "Ren", "Gon",
			"HxH", "Uvo", "Ant"
		]
		for text in incorrect_OTC_values:
			self.assertRaises(
				sqlite3.IntegrityError,
				self.cur.execute,
				query_template.format(text))
	
	def test_Leki_dawka_CHECK_only_positive_values(self):
		"""dawka is a real strictly positive number."""
		query_template = "INSERT INTO Leki(bloz, dawka) VALUES (1122334, {})"
		dawka_bad_values = [-0.00001, -0.33, -17.5, 0.0]
		for number in dawka_bad_values:
			self.assertRaises(
				sqlite3.IntegrityError,
				self.cur.execute,
				query_template.format(number))


class DataBasePopulation(unittest.TestCase):
	
	def setUp(self):
		"""Create database and connect to it."""
		db.create_db()
		db.populate_Leki()
		db.populate_Producenci()
		if os.path.exists("substances.db"):
			self.con = sqlite3.connect("substances.db")
			self.cur = self.con.cursor()
		else:
			raise Exception("Failed to connect, substances.db does not exist.")
	
	def tearDown(self):
		"""Close connection to db and remove its file."""
		self.con.close()
		current_directory = os.getcwd()
		(head, tail) = os.path.split(current_directory)
		#print(f"\nbefore the if\n{head=} {tail=}")
		if tail == "tests":
			os.chdir("..")
			(head, tail) = os.path.split(current_directory)
			#print("Inside the if:")
			#print(f"{head=} {tail=}")
		#print("after the if")
		#print(f"substances.db exists: {os.path.exists("substances.db")}")
		if os.path.exists("substances.db"):
			os.unlink("substances.db")
		else:
			raise Exception(f"no file named 'substances.db' inside {tail}")

	def test_existance_of_table_Leki(self):
		"""Table Leki exists with at least one tuple."""
		query = """
			SELECT *
			FROM Leki
			WHERE bloz = 6488741;
		"""
		res = self.cur.execute(query)
		a_tuple = (
			6488741, 'Ibufen Junior', 'ibuprofen',
			'kapsułki miękkie', 200, 'Tak',
			'Jest to preparat o działaniu ogólnym zawierający niesteroidowy lek przeciwzapalny.',
			'Zakłady Farmaceutyczne POLPHARMA S.A.',
			'ul. Pelplińska 19, 83-200, Starogard Gdański'
		)
		self.assertTupleEqual(a_tuple, res.fetchone())
	
	def test_existance_of_table_Producenci(self):
		"""Table Producenci exists with at least one tuple."""
		query = """
			SELECT *
			FROM Producenci
			WHERE
				(producent LIKE '%Polpharma%') AND (siedziba LIKE '%Pelplińska 19%Starogard Gdański');
		"""
		res = self.cur.execute(query)
		a_tuple = (
			'Zakłady Farmaceutyczne POLPHARMA S.A.',
			'ul. Pelplińska 19, 83-200, Starogard Gdański',
			'Sebastian Szymanek', 1935
		)
		self.assertTupleEqual(a_tuple, res.fetchone())


if __name__ == "__main__":
	unittest.main()