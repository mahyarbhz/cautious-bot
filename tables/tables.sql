CREATE TABLE users (
  idusers INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NULL,
  score VARCHAR(45) NULL,
  guild VARCHAR(45) NULL,
  PRIMARY KEY (idusers));

CREATE TABLE responces (
  id INT NOT NULL AUTO_INCREMENT,
  gen_id INT NULL,
  guild VARCHAR(45) NULL,
  response_to VARCHAR(45) NULL,
  UNIQUE INDEX gen_id_UNIQUE (gen_id ASC) VISIBLE,
  PRIMARY KEY (`id`));

CREATE TABLE responce (
  id INT NOT NULL AUTO_INCREMENT,
  response_id INT NULL,
  text VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
