CREATE DATABASE IF NOT EXISTS artists_db;
USE artists_db;

CREATE TABLE IF NOT EXISTS artists (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `genre` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS albums (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `trackCount` INT NOT NULL,
  `explicit` VARCHAR(45) NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  `artistName` VARCHAR(255) NOT NULL,
  `artistId` INT NOT NULL,
  `releaseDate` DATE NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));
	
CREATE TABLE IF NOT EXISTS songs (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `explicit` VARCHAR(45) NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  `artistName` VARCHAR(255) NOT NULL,
  `artistId` INT NOT NULL,
  `albumName` VARCHAR(255) NOT NULL,
  `albumId` INT NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  `durationMinutes` REAL NOT NULL,
  PRIMARY KEY (`id`));