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
	
-- CREATE TABLE songs (
--   `idSong` INT NOT NULL AUTO_INCREMENT,
--   `nameSong` VARCHAR(255) NOT NULL,
--   `explicit` VARCHAR(45) NOT NULL,
--   `genre` VARCHAR(45) NOT NULL,
--   `idSongItunes` BIGINT NOT NULL,
--   `nameArtistSong` VARCHAR(255) NOT NULL,
--   `nameAlbumSong` VARCHAR(255) NOT NULL,
--   `idAlbumSong` INT NOT NULL,
--   PRIMARY KEY (`idSong`),
--   INDEX `idAlbumSong_idx` (`idAlbumSong` ASC) VISIBLE,
--   CONSTRAINT `idAlbumSong`
--     FOREIGN KEY (`idAlbumSong`)
--     REFERENCES albuns (`idAlbum`)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE);