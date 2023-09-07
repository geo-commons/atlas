from django.test import TestCase

from webservice.models import Layer, Category


class TestLayerModel(TestCase):
    def setUp(self):
        self.closed_dataset = Layer.objects.create(
            slug="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            published=False,
            layer_type=Category.objects.create(
                title='theme_layer'))
        self.open_dataset = Layer.objects.create(
            title="Purm",
            layer_name="",
            closed_dataset=False,
            _popup_attributes="test\ntest1",
            layer_type=Category.objects.create(
                title='base_layer'))

    def test_layer_name(self):
        self.assertEqual(self.closed_dataset.layer_name,
                         "topp:Purm_Stembureaus_2018")

    def test_popup_attributest(self):
        self.assertEqual(self.open_dataset.popup_attributes,
                         "popupAttributes: ['test', 'test1']")

    def test_non_popup_attributest(self):
        self.assertEqual(self.closed_dataset.popup_attributes, '')

    def test_is_published(self):
        self.assertFalse(self.closed_dataset.is_published)
        self.assertFalse(self.open_dataset.is_published)
        self.open_dataset.published = True
        self.closed_dataset.published = True
        self.assertTrue(self.closed_dataset.is_published)
        self.assertTrue(self.open_dataset.is_published)

    def test_is_closed_dataset(self):
        self.assertTrue(self.closed_dataset.is_closed_dataset)
        self.assertFalse(self.open_dataset.is_closed_dataset)

    def test_slddiv(self):
        self.assertEqual(self.closed_dataset.slddiv,
                         "sld_div_purm_stembureaus_2018")

    def test_infodiv(self):
        self.assertEqual(self.closed_dataset.infodiv,
                         "info_purm_stembureaus_2018")

    def test_sld(self):
        self.assertEqual(self.closed_dataset.sld, "sld_purm_stembureaus_2018")

    def test_legend(self):
        self.assertEqual(self.closed_dataset.legend,
                         "lgn_purm_stembureaus_2018")

    def test_filterid(self):
        self.assertEqual(self.closed_dataset.filterid,
                         "flt_purm_stembureaus_2018")

    def test_filterdataid(self):
        self.assertEqual(self.closed_dataset.filterdataid,
                         "data_purm_stembureaus_2018")

    def test_datazoekid(self):
        self.assertEqual(self.closed_dataset.datazoekid,
                         "zoek_data_purm_stembureaus_2018")

    def test_params(self):
        self.assertEqual(self.closed_dataset.params,
                         "{'layers': 'topp:Purm_Stembureaus_2018'}")

    def test_source(self):
        self.assertEqual(self.closed_dataset.source, """
source: new ol.source.TileWMS({
    projection: 'EPSG:28992',
    url: '',
    params: {'layers': 'topp:Purm_Stembureaus_2018'},
    serverType: 'geoserver'
})""")


class TestLayerOrdering(TestCase):
    def setUp(self):
        self.stembureaus = Layer.objects.create(
            slug="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            published=True,
            ordering=10)
        self.purm = Layer.objects.create(
            title="Purm",
            layer_name="",
            closed_dataset=False,
            published=True,
            _popup_attributes="test\ntest1",
            ordering=0)
        self.purm2 = Layer.objects.create(
            title="Purm2",
            layer_name="",
            closed_dataset=False,
            published=True,
            _popup_attributes="test\ntest1",
            ordering=0)

    def test_ordering(self):
        layers = list(Layer.objects.all())
        self.assertListEqual(
            [self.purm, self.purm2, self.stembureaus],
            layers)
