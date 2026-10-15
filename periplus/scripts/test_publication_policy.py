"""Observable acceptance regressions for final maps and reference links."""
import unittest
from publication_policy import audit_map_capture,audit_final_reference_links,audit_photo_resolution,audit_pdf_map_resolution

class PublicationPolicyTests(unittest.TestCase):
    def asset(self):
        return dict(file='maps/map_a.png',provider='Google Maps',capture_method='browser_screenshot',capture_url='https://www.google.com/maps/@40,140,16z',viewport_css=[1000,700],device_scale_factor=2,screenshot_pixels=[2000,1400],captured_on='2026-10-15',attribution_visible=True,print_readability_checked=True)
    def test_native_google_capture(self):self.assertEqual(audit_map_capture(self.asset(),(2000,1400)),[])
    def test_native_map_pixels_survive_final_pdf(self):
        a={**self.asset(),'kind':'map'}
        self.assertEqual(audit_pdf_map_resolution([a],[dict(width=2000,height=1400)]),[])
    def test_pdf_downsampling_is_rejected(self):
        a={**self.asset(),'kind':'map'}
        self.assertTrue(audit_pdf_map_resolution([a],[dict(width=1244,height=870)]))
    def test_low_resolution_rejected(self):self.assertTrue(audit_map_capture(self.asset(),(900,600)))
    def test_upscaled_capture_rejected(self):
        a=self.asset();a['viewport_css']=[500,350];self.assertTrue(audit_map_capture(a,(2000,1400)))
    def test_provider_substitution_rejected(self):
        a=self.asset();a['provider']='GSI';self.assertTrue(audit_map_capture(a,(2000,1400)))
    def test_attribution_review_required(self):
        a=self.asset();a['attribution_visible']=False;self.assertTrue(audit_map_capture(a,(2000,1400)))
    def test_media_source_excluded_but_travel_source_kept(self):
        photo=dict(source_url='https://museum.jp/visit',download_url='https://museum.jp/photo.jpg',source_is_travel_resource=True)
        good='### References\n[Hours](https://museum.jp/visit)'
        self.assertEqual(audit_final_reference_links(good,[photo]),[])
        self.assertTrue(audit_final_reference_links(good+'\n[Photo](https://museum.jp/photo.jpg)',[photo]))
    def test_internal_provenance_and_caption_do_not_pollute_final_list(self):
        text='Photo credit [required link](https://creativecommons.org/licenses/by/4.0/).\n### References\n[Railway](https://www.jreast.co.jp/)'
        self.assertEqual(audit_final_reference_links(text,[]),[])
    def test_repository_or_credit_appendix_rejected(self):
        self.assertTrue(audit_final_reference_links('### References\n[Image](https://commons.wikimedia.org/wiki/File:A.jpg)',[]))
        self.assertTrue(audit_final_reference_links('### Image and Map Credits\n[Source](https://museum.jp/)',[]))
    def test_native_small_photo_uses_real_print_resolution(self):
        a=dict(file='photos/native.jpg',native_resolution=[394,261],print_width_cm=4,small_print_reviewed=True)
        self.assertEqual(audit_photo_resolution(a,(394,261)),[])
        a['print_width_cm']=8;self.assertTrue(audit_photo_resolution(a,(394,261)))
        a['print_width_cm']=4;a['native_resolution']=[800,600];self.assertTrue(audit_photo_resolution(a,(394,261)))

if __name__=='__main__':unittest.main()
