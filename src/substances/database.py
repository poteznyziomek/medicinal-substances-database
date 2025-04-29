import sqlite3 as sql

def create_db():
	"""Create a substances database and define its tables."""
	connection = sql.connect("substances.db")
	cur = connection.cursor()
	create_schema_Leki = """
		CREATE TABLE Leki(
			bloz INT PRIMARY KEY NOT NULL CHECK
				(bloz >= 1000000 AND bloz < 10000000),
			nazwaHandlowa VARCHAR(255) UNIQUE,
			substancjaAktywna VARCHAR(255),
			postac VARCHAR(255),
			dawka DOUBLE PRECISION CHECK
				(dawka > 0),
			OTC VARCHAR(3) CHECK
				(OTC IN ('Nie', 'Tak', 'Rpw')),
			zastosowanie VARCHAR(255),
			producent VARCHAR(255),
			UNIQUE (substancjaAktywna, postac, dawka)
		);
	"""
	create_schema_Producenci = """
		CREATE TABLE Producenci(
			producent VARCHAR(255) NOT NULL,
			siedziba VARCHAR(255) NOT NULL,
			prezes VARCHAR(255),
			rokZalozenia INT,
			PRIMARY KEY (producent, siedziba)
		);
	"""
	create_schema_BlozSiedziba = """
		CREATE TABLE BlozSiedziba(
			bloz INT NOT NULL CHECK
				(bloz >= 1000000 AND bloz < 10000000),
			siedziba VARCHAR(255) NOT NULL,
			PRIMARY KEY (bloz, siedziba)
		);
	"""
	
	cur.execute(create_schema_Leki)
	cur.execute(create_schema_Producenci)
	cur.execute(create_schema_BlozSiedziba)
	connection.commit()
	connection.close()

def populate_Leki():
	"""Insert tuples into Leki table."""
	connection = sql.connect("substances.db")
	cur = connection.cursor()
	new_tuples = """
		INSERT INTO Leki
		VALUES
			(6488741, 'Ibufen Junior', 'ibuprofen', 'kapsułki miękkie', 200, 'Tak', 'Jest to preparat o działaniu ogólnym zawierający niesteroidowy lek przeciwzapalny.', 'Zakłady Farmaceutyczne POLPHARMA S.A.'),
			(6840052, 'Ketonal', 'ketoprofen', 'roztwór do wsztrzykiwań', 50, 'Nie', 'Jest to preparat o działaniu ogólnym zawierający niesteroidowy lek przeciwzapalny.', 'Sandoz Polska sp. z o.o.'),
			(9680481, 'Ibuprom', 'ibuprofen', 'tabletki powlekane', 200, 'Tak', 'Jest to preparat o działaniu ogólnym zawierający niesteroidowy lek przeciwzapalny.', 'US Pharmacia Sp. z o.o.'),
			(4141109, 'Amol', 'olejek goździkowy + olejek cynamonowy + olejek cytrynowy + olejek cytronelowy + olejek lawendowy + olejek miętowy + mentol', 'płyn doustny oraz do stosowania na skórę', 32.13, 'Tak', 'Tradycyjny preparat w postaci płynu do stosowania zewnętrznego, na skórę lub wewnętrznego, doustnie, zawierający mieszaninę olejków eterycznych.', 'Takeda Pharma'),
			(1933641, 'Apap', 'paracetamol', 'tabletki', 500, 'Tak', 'Lek przeciwbólowy i przeciwgorączkowy', 'US Pharmacia Sp. z o.o.'),
			(3091821, 'Nimesil', 'nimesulid', 'granulat do sporządzania zawiesiny doustnej', 100, 'Nie', 'Jest to preparat o działaniu ogólnym zawierający niesteroidowy lek przeciwzapalny', 'Laboratori Guidotti S.p.A'),
			(2053895, 'Izotek', 'izotretynoina', 'kapsułki miękkie', 0.75, 'Nie', 'Pochodna wit. A', 'InPharm Sp. z o.o.'),
			(9840799, 'Aspirin', 'kwas acetylosalicylowy', 'tabletki', 1000, 'Tak', 'Niesteroidowy lek przeciwzapalny o działaniu przecibólowym, przeciwgorączkowym i przeciwzapalnym oraz hamującym agregację płytek krwi', 'Bayer'),
			(6290601, 'Fentanyl WZF', 'fentanyl', 'roztwór do wstrzykiwań', 0.075, 'Nie', 'Opioidowy lek przeciwbólowy', 'Zakłady Farmaceutyczne POLPHARMA S.A.'),
			(3373322, 'Alprazolam Aurovitas', 'alprazolam', 'tabletki', 0.38, 'Nie', 'Lek przeciwlękowy, pochodna benzodiazepiny.', 'Aurovitas Pharma Polska Sp. z o.o.');
	"""
	cur.execute(new_tuples)
	connection.commit()
	connection.close()

def populate_Producenci():
	"""Insert tuples into Producenci table."""
	connection = sql.connect("substances.db")
	cur = connection.cursor()
	new_tuples = """
		INSERT INTO Producenci
		VALUES
			('Zakłady Farmaceutyczne POLPHARMA S.A.', 'ul. Pelplińska 19, 83-200, Starogard Gdański', 'Sebastian Szymanek', 1935),
			('Sandoz Polska sp. z o.o.', 'ul. Domaniewska 50 c, 02-672 Warszawa, Polska', 'Karolina Demus', 2010),
			('US Pharmacia Sp. z o.o.', 'Ziębicka 40, 50-507, Wrocław', 'Marcin Szałapski', 1997),
			('Takeda Pharma', '1-1, Nihonbashi-Honcho 2-chome, Chuo-ku, Tokyo, 103-8668, Japan', 'Christophe Weber', 1781),
			('Laboratori Guidotti S.p.A', 'Via Livornese 897, 56122 Piza, Włochy', 'Luigi Duca',1914),
			('InPharm Sp. z o.o.', 'ul. Chełmżyńska 249, 04-458 Warszawa', 'Sławomir Bernaciak', 2006),
			('Bayer', 'Salegaster Ch 1, 06803 Bitterfeld-Wolfen, Niemcy', 'Bill Anderson', 1863),
			('Aurovitas Pharma Polska Sp. z o.o.', 'Warszawa, Polska', 'Michał Jakubowski', 1986),
			('Polfa Warszawa S.A.', 'Warszawa, Polska', 'Krzysztof Raczyński', 1961),
			('GlaxoSmithKline Pharmaceuticals', 'Brentford, Wielka Brytania', 'Emma Walmsley', 2000);
	"""
	cur.execute(new_tuples)
	connection.commit()
	connection.close()

def populate_BlozSiedziba():
	"""Insert tuples into BlozSiedziba table."""
	connection = sql.connect("substances.db")
	cur = connection.cursor()
	new_tuples = """
		INSERT INTO BlozSiedziba
		VALUES
			(6488741, 'ul. Pelplińska 19, 83-200, Starogard Gdański'),
			(6840052, 'ul. Domaniewska 50 c, 02-672 Warszawa, Polska'),
			(9680481, 'Ziębicka 40, 50-507, Wrocław'),
			(4141109, '1-1, Nihonbashi-Honcho 2-chome, Chuo-ku, Tokyo, 103-8668, Japan'),
			(1933641, 'Ziębicka 40, 50-507, Wrocław'),
			(3091821, 'Via Livornese 897, 56122 Piza, Włochy'),
			(2053895, 'ul. Chełmżyńska 249, 04-458 Warszawa'),
			(9840799, 'Salegaster Ch 1, 06803 Bitterfeld-Wolfen, Niemcy'),
			(6290601, 'ul. Pelplińska 19, 83-200, Starogard Gdański'),
			(3373322, 'Warszawa, Polska');
	"""
	cur.execute(new_tuples)
	connection.commit()
	connection.close()

def initialize():
	"""Create substances database and populate it."""
	create_db()
	populate_Leki()
	populate_Producenci()
	populate_BlozSiedziba()