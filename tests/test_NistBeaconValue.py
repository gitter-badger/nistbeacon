from unittest import TestCase

from nist_randomness_beacon import NistBeaconValue


class TestNistBeaconValue(TestCase):
    def setUp(self):
        # noinspection SpellCheckingInspection
        self.sample_nist_xml = ('<record>'
                                '<version>Version 1.0</version>'
                                '<frequency>60</frequency>'
                                '<timeStamp>1447873020</timeStamp>'
                                '<seedValue>'
                                '6189C4FF1F17ED41F9FF017CEB82DB2579193FBBB'
                                '867B95E7FEBA52E74C937377626C522454C6223B2'
                                '5C007BF09C4B3AB55D24CFE1EB8F67C306FA75147'
                                'E1CD2'
                                '</seedValue>'
                                '<previousOutputValue>'
                                'F4F571DFBA7DA2D3872AF1696B6A32B5039EB9CAB'
                                'F03CBB17EAB095D83B1483A12CE2D0347BEAF2709'
                                'CA0BAC0EB78C330D20CD3BE2FBEC2F7816AB2BB95'
                                '3AA3D'
                                '</previousOutputValue>'
                                '<signatureValue>'
                                'F029F1A167DDBC17C041B9EB0A6AF2BC417D42C75'
                                '001E39C2F9E2281AB9533B34ACBB584414AC10C20'
                                '322F72C53D6425F3C595ECA31A0B26A23D0573DCA'
                                '6DEADE09D02214A7F9AF7EC0424D69B26EAF7269C'
                                '648349AD189D90A43D67576BF4B00035118F1AD93'
                                '9D228489A37EF822FEB04C2B4D1676B1041EC9288'
                                '3101150AAF7747EC88FE176BCA1B289E608E04CAF'
                                '4CF47BE16A1B6243F8330E539740B9F6EB70A7A8E'
                                '06777932B98617745AA2B545EFFA0DAA8DE016D00'
                                'B55B01AEC91000508ACC4908D17A17311C68D156D'
                                '63A03110250CB959A023BA75C700FE4EB43543DC1'
                                'AC35781FF91D72AA7FE467F83569318C83D316801'
                                'CC7159E83E2C306ADC2D'
                                '</signatureValue>'
                                '<outputValue>'
                                '2BE1468DF2E4081306002B9F9E344C7826DDC2255'
                                '83ED7FACC8804086867457DD4F4BD2DF9F5CE4B88'
                                'DF6E30E4838F15168946BE18DFF596E667EC543AC'
                                '08F54'
                                '</outputValue>'
                                '<statusCode>0</statusCode>'
                                '</record>'
                                )

    def test_from_xml(self):
        expected_node = None
        actual_node = NistBeaconValue.from_xml(self.sample_nist_xml)
        pass

    def test_noop(self):
        self.assertIsInstance(self.sample_nist_xml, str)
