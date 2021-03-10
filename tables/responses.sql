CREATE TABLE responces (
  id INT NOT NULL AUTO_INCREMENT,
  gen_id INT NULL,
  guild VARCHAR(45) NULL,
  response_to VARCHAR(45) NULL,
  UNIQUE INDEX gen_id_UNIQUE (gen_id ASC) VISIBLE,
  PRIMARY KEY (`id`));