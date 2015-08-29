CREATE TABLE languages (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(255),
	PRIMARY KEY (id)
);

CREATE TABLE books (
	id int NOT NULL AUTO_INCREMENT,
	title varchar(255),
	author varchar(255),
	releaseDate varchar(255),
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
	wordNumberInLine int,
	originalWord varchar(255),
	originalWordLower varchar(255),
	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (bookId) REFERENCES books(id),
	PRIMARY KEY (wordId, bookId, wordNumber)
);

CREATE TABLE groupWords (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(255),
	dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
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
	name varchar(255),
	dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);

CREATE TABLE wordsInPhrases (
	wordId int,
	phraseId int,
	orderNumber int,
	wordText varchar(255),
	wordTextLower varchar(255),
	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (phraseId) REFERENCES phrases(id),
	PRIMARY KEY (orderNumber, phraseId)
);

CREATE TABLE dataMining (
  bookId int,
  apperanceCount int,
  wordId1 int,
  wordId2 int,
  dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (wordId1) REFERENCES words(id),
	FOREIGN KEY (wordId2) REFERENCES words(id),
	FOREIGN KEY (bookId) REFERENCES books(id),
	PRIMARY KEY (wordId1, wordId2, bookId)
);