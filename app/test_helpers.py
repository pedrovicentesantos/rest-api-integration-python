import unittest
from unittest import mock

from helpers import get_artist_id, get_type_from_id, is_on_itunes, on_db
from db_connect import connect_to_db
import mysql.connector

class HelpersTestCase(unittest.TestCase):
  # Testes para função: get_artist_id(id)
  def test_get_artist_id_type_response_artist_found(self):
    result = get_artist_id("dua lipa")
    self.assertIsInstance(result,tuple)

  def test_get_artist_id_type_response_artist_not_found(self):
    result = get_artist_id("marilia asdsa")
    self.assertIsInstance(result,tuple)

  def test_get_artist_id_type_response_input_not_str(self):
    result = get_artist_id(2)
    self.assertIsInstance(result,str)
    self.assertNotIsInstance(result,tuple)

    result = get_artist_id((2,1))
    self.assertIsInstance(result,str)
    self.assertNotIsInstance(result,tuple)

    result = get_artist_id({"argument"})
    self.assertIsInstance(result,str)
    self.assertNotIsInstance(result,tuple)
  
  def test_get_artist_id_type_response_results(self):
    result = get_artist_id("marilia asdsa")
    for r in result:
      self.assertIsInstance(r, str)

    result = get_artist_id("dua lipa")
    self.assertIsInstance(result[0],int)
    self.assertIsInstance(result[1],str)

  # Testes para função: get_type_from_id(id, searchType)
  def test_get_type_from_id_search_artist_found(self):
    result = get_type_from_id(1031397873,"song")
    self.assertIsInstance(result, list)

    result = get_type_from_id(1031397873,"album")
    self.assertIsInstance(result, list)

  def test_get_type_from_id_search_albuns_artist_not_found(self):
    result = get_type_from_id(2,"album")
    self.assertIsInstance(result, list)

    result = get_type_from_id(2,"song")
    self.assertIsInstance(result, list)

  def test_get_type_from_id_search_input_searchType_not_str(self):
    result = get_type_from_id(1031397873,2)
    self.assertIsInstance(result, str)

    result = get_type_from_id(1031397873,(2,1))
    self.assertIsInstance(result, str)

    result = get_type_from_id(1031397873,{(2,1)})
    self.assertIsInstance(result, str)

    result = get_type_from_id(1,3)
    self.assertIsInstance(result, str)

  def test_get_type_from_id_wrong_url(self):
    result = get_type_from_id("teste", "album")
    self.assertIsInstance(result,str)

    result = get_type_from_id(("teste",1), "album")
    self.assertIsInstance(result,str)

    result = get_type_from_id({("teste",1)}, "song")
    self.assertIsInstance(result,str)

  #Testes para função: is_on_itunes(artist) -> type(artist) == str
  @mock.patch('helpers.get_artist_id')
  def test_is_on_itunes(self,mock):
    # Testa se o mock foi chamado dentro da função que quero testar
    result = is_on_itunes(mock())
    self.assertTrue(mock.called)

    # Testa se o resultado é uma tupla
    # Testa se retorna True pois esse artista existe
    mock.return_value = (1031397873,"Dua Lipa")
    result = is_on_itunes(mock())
    self.assertIsInstance(result,tuple)
    self.assertTrue(result[0])
    
    # Testa se o resultado é uma tupla
    # Testa se retorna False pois nesse caso não tem ID de artista
    mock.return_value = ("","Teste")
    result = is_on_itunes(mock())
    self.assertIsInstance(result,tuple)
    self.assertFalse(result[0])

    # Testa se retorna uma string quando recebe um erro
    mock.return_value = "Error"
    result = is_on_itunes(mock())
    self.assertIsInstance(result,str)
    self.assertNotIsInstance(result,tuple)

    # Testa se cai na exceção quando não recebe uma string
    # mock.return_value = 2
    result = is_on_itunes(2)
    self.assertRaises(Exception)
    result = is_on_itunes([2])
    self.assertRaises(Exception)
    result = is_on_itunes({2})
    self.assertRaises(Exception)

  # Testes para função: connect_to_db()
  @mock.patch('mysql.connector.connect')
  def test_connect_to_db(self,mock):

    # Quando conecta
    mock.return_value.is_connected.return_value = True
    result = connect_to_db()
    self.assertIsNotNone(result)
    self.assertIsInstance(result,unittest.mock.MagicMock)

    # Quando não conecta
    mock.return_value.is_connected.return_value = False
    result = connect_to_db()
    self.assertIsNone(result)
    self.assertNotIsInstance(result,unittest.mock.MagicMock)

    # # Quando ocorre uma exceção
    mock.side_effect = Exception()
    result = connect_to_db()
    self.assertIsNotNone(result)
    self.assertRaises(Exception)
    self.assertIsInstance(result,str)
    self.assertRegex(result,"Error:*")

if __name__ == '__main__':
    unittest.main()