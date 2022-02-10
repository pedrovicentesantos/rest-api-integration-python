CREATE TABLE IF NOT EXISTS artists (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `genre` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));

-- CREATE TABLE IF NOT EXISTS albuns (
--   `idAlbum` INT NOT NULL AUTO_INCREMENT,
--   `nameAlbum` VARCHAR(255) NOT NULL,
--   `trackCount` INT NOT NULL,
--   `explicit` VARCHAR(45) NOT NULL,
--   `genre` VARCHAR(45) NOT NULL,
--   `idAlbumItunes` BIGINT NOT NULL,
--   `nameArtistAlbum` VARCHAR(255) NOT NULL,
--   `idArtistAlbum` INT NOT NULL,
--   PRIMARY KEY (`idAlbum`),
--   INDEX `idArstistAlbum_idx` (`idArtistAlbum` ASC) VISIBLE,
--   CONSTRAINT `idArtistAlbum`
--     FOREIGN KEY (`idArtistAlbum`)
--     REFERENCES artists (`idArtist`)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE);
	
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