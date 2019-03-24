from dexstore.utils import assets_from_string


def test_assets_from_string():
    assert assets_from_string('USD:DST') == ['USD', 'DST']
    assert assets_from_string('DSTBOTS.S1:DST') == ['DSTBOTS.S1', 'DST']
