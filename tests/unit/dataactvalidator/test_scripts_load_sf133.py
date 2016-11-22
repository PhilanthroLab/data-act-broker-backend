import pandas as pd

from dataactvalidator.scripts import load_sf133


# These columns are used to group SF133 rows when filling in missing data.
# It's everything but 'line' and 'amount'
FINGERPRINT_COLS = [
    'availability_type_code', 'sub_account_code',
    'allocation_transfer_agency', 'fiscal_year', 'beginning_period_of_availa',
    'ending_period_of_availabil', 'main_account_code', 'agency_identifier',
    'period', 'created_at', 'updated_at', 'tas']


def test_fill_blank_sf133_lines_types():
    """Validate that floats aren't downgraded to ints in the pivot_table
    function (that'd be a regression)."""
    data = pd.DataFrame(
        # We'll only pay attention to two of these fields
        [[1440, 3041046.31] + list('ABCDEFGHIJKL')],
        columns=['line', 'amount'] + FINGERPRINT_COLS
    )
    result = load_sf133.fill_blank_sf133_lines(data)
    assert result['amount'][0] == 3041046.31


def test_fill_blank_sf133_lines():
    """This function should fill in missing data if line numbers (i.e. rows)
    of the input are missing"""
    data = pd.DataFrame(
        # Using the letters of 'FINGERPRINTX' to indicate how to group SF133
        # rows. FINGERPRINT1 has rows for line numbers 1 and 2, while
        # FINGERPRINT2 has rows for line numbers 2 and 3. We want both to have
        # line numbers 1 through 3
        [[1, 1] + list('FINGERPRINT1'),
         [2, 2] + list('FINGERPRINT1'),
         [2, 2] + list('FINGERPRINT2'),
         [3, 3] + list('FINGERPRINT2')],
        columns=['line', 'amount'] + FINGERPRINT_COLS
    )
    result = load_sf133.fill_blank_sf133_lines(data)
    assert list(sorted(result[result['line'] == 1]['amount'])) == [0.0, 1.0]
    assert list(sorted(result[result['line'] == 2]['amount'])) == [2.0, 2.0]
    assert list(sorted(result[result['line'] == 3]['amount'])) == [0.0, 3.0]
