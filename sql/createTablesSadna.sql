CREATE TABLE languages (
	id int,
	name varchar(255),
	PRIMARY KEY (id)
);

CREATE TABLE books (
	id int,
	title varchar(255),
	author varchar(255),
	releaseDate DATE,
	language int,
	fileLocation varchar(255),
	FOREIGN KEY (language) REFERENCES languages(id),
	PRIMARY KEY (id)
);	

CREATE TABLE words (
	id int,
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
	PRIMARY KEY (wordId, bookId)
);

CREATE TABLE groupWords (
	id int,
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