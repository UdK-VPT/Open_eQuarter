from django.test import TestCase

from crow.models import Layer, OeQLayer


class LayerModelTest(TestCase):

    def test_saving_and_retrieving_layers(self):
        layer = Layer()
        layer.name = 'Heinrichstraße'
        layer.save()

        field = '0106000020E6100000010000000103000000010000000D000000345E9B33DEE02A4021042E35A73F4A406E34F58EDBE02A4049D9C282A63F4A40FE6E470AEEE02A40C83641FAA43F4A4001F4C0C1F2E02A40D5CA0096A43F4A40FEF274DEF4E02A40C0D92C69A43F4A40BA226C80F4E02A40533E8F51A43F4A40B3564489E6E02A408649CCD2A03F4A40F75BACC0E4E02A40DFA59AFBA03F4A40EEFA23D5DFE02A407C48F760A13F4A403E8F77C8C2E02A40471F33B7A33F4A403675CCD4CFE02A4048AE34FEA63F4A40ECE2F4F8D3E02A4023296608A83F4A40345E9B33DEE02A4021042E35A73F4A40'
        oeq_layer = OeQLayer(geom=field)
        oeq_layer.layer = layer
        oeq_layer.save()

        saved_layer = Layer.objects.first()
        saved_oeq_layer = OeQLayer.objects.first()
        self.assertEqual(saved_layer.name, 'Heinrichstraße')
        self.assertEqual(saved_layer.features()[0], saved_oeq_layer)

    def test_commenting_a_layer(self):
        layer = Layer()
        layer.name = 'Heinrichstraße'
        layer.comment = 'This is a comment'
        layer.save()

        saved_layer = Layer.objects.first()
        self.assertEqual(layer.comment, 'This is a comment')

