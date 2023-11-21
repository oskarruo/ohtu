import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()

        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id >= 1 and tuote_id <=5:
                return 10
            if tuote_id == 6:
                return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "juusto", 10)
            if tuote_id == 3:
                return Tuote(3, "margariini", 15)
            if tuote_id == 4:
                return Tuote(4, "hyvä suomalainen leipä", 20)
            if tuote_id == 5:
                return Tuote(5, "tavallinen jogurtti", 6)
            if tuote_id == 6:
                return Tuote(6, "halpa, makea, epäterveellinen mansikkajogurtti", 1)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        self.kauppa.aloita_asiointi()
    
    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_ostos_kutsuu_metodia_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kahden_eri_tuotteen_osto_kutsuu_metodia_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 25)

    def test_kahden_saman_tuotteen_osto_kutsuu_metodia_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.lisaa_koriin(4)
        self.kauppa.lisaa_koriin(4)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 40)

    def test_varastossa_olevan_tuotteen_ja_loppuneen_tuotteen_ostaminen_kutsuu_metodia_tilisiirto_oikeilla_parametreillla(self):
        self.kauppa.lisaa_koriin(5)
        self.kauppa.lisaa_koriin(6)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 6)

    def test_metodin_aloita_asiointi_kutsuminen_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pätkä", "123456")

        self.pankki_mock.tilisiirto.assert_called_with("pätkä", 42, "123456", "33333-44455", 10)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())
        
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_mock)

        self.kauppa.aloita_asiointi()

        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(4)
        self.kauppa.tilimaksu("pätkä", "123456")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 2)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(5)
        self.kauppa.tilimaksu("justiina", "1234567")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_tuote_korista(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        
        self.kauppa.poista_korista(2)

        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)
