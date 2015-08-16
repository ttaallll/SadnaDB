CREATE TABLE languages (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(255),
	PRIMARY KEY (id)
);

CREATE TABLE books (
	id int NOT NULL AUTO_INCREMENT,
	title varchar(255),
	author varchar(255),
	releaseDate DATE,
	language int,
	fileLocation varchar(255),
	FOREIGN KEY (language) REFERENCES languages(id),
	PRIMARY KEY (id)
);	

CREATE TABLE words (
	id int NOT NULL AUTO_INCREMENT,
	word varchar(255),
	
	PRIMARY KEY (id)
);

CREATE TABLE wordsInBooks (
	wordId int,
	bookId int,
	lineNumber int,
	wordNumber int,
	characterLocation int,
	sentenceNumber int,
	paragraphNumber int,
	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (bookId) REFERENCES books(id),
	PRIMARY KEY (wordId, bookId, wordNumber)
);

CREATE TABLE groupWords (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(255),
	dateCreated DATE,
	PRIMARY KEY (id)
);

CREATE TABLE wordsInGroupWords (
	wordId int,
	groupWordId int,
	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (groupWordId) REFERENCES groupWords(id),
	PRIMARY KEY (wordId, groupWordId)
);

CREATE TABLE phrases (
	id int NOT NULL AUTO_INCREMENT,
	dateCreated DATE,
	PRIMARY KEY (id)
);

CREATE TABLE wordsInphrases (
	wordId int,
	phraseId int,
	orderNumber int,
	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (phraseId) REFERENCES phrases(id),
	PRIMARY KEY (wordId, phraseId)
);