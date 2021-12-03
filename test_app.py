from unittest import TestCase, mock, main
from app import build_chord, get_chord_type, char_is_chord, parse_tab_page, build_search_url, get_tab_page_url

class TestStringMethods(TestCase):

        def test_build_chord(self):
                chord = build_chord("G")
                self.assertEqual(chord, '<span class="_3PpPJ OrSDI" data-name="G" style="color: rgb(0, 0, 0);">G</span>')


        def test_get_chord_type(self):
                bm_chord_type, bm_chord_len = get_chord_type("[ch]Bm[/ch]",0)
                self.assertEqual(bm_chord_type, "Bm")
                self.assertEqual(bm_chord_len, 11)
                b_chord_type, b_chord_len = get_chord_type("[ch]B[/ch]",0)
                self.assertEqual(b_chord_type, "B")
                self.assertEqual(b_chord_len, 10)


        def test_char_is_chord(self):
                html = "[ch]foobar"
                self.assertTrue(char_is_chord(html,0))
                html_two = "foobar"
                self.assertFalse(char_is_chord(html_two,0))


        def test_build_search_url(self):
                search_url = build_search_url("Better Together", "Jack Johnson")
                self.assertEqual(search_url, "https://www.ultimate-guitar.com/search.php?title=Jack%20Johnson%20Better%20Together&page=1&type=300")


if __name__ == '__main__':
    main()