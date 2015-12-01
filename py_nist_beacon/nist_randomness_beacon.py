import requests
from requests.exceptions import RequestException

import py_nist_beacon.nist_beacon_constants as cn
from py_nist_beacon.nist_randomness_beacon_value import (
    NistRandomnessBeaconValue
)


class NistRandomnessBeacon(object):
    NIST_BASE_URL = "https://beacon.nist.gov/rest/record"

    @classmethod
    def _query_nist(cls, url_data: str) -> NistRandomnessBeaconValue:
        try:
            r = requests.get(
                "{0}/{1}".format(
                    cls.NIST_BASE_URL,
                    url_data,
                )
            )

            if r.status_code is requests.codes.OK:
                return NistRandomnessBeaconValue.from_xml(r.text)
            else:
                return None
        except RequestException:
            return None

    @classmethod
    def chain_check(cls, timestamp: int) -> bool:
        """
        Given a record timestamp, verify the chain integrity.

        :param timestamp: UNIX time / POSIX time / Epoch time
        :return: 'True' if the timestamp fits the chain. 'False' otherwise.
        """

        # Creation is messy.
        # You want genius, you get madness; two sides of the same coin.
        # ... I'm sure this can be cleaned up. However, let's test it first.

        record = cls.get_record(timestamp)

        if isinstance(record, NistRandomnessBeaconValue) is False:
            # Don't you dare try to play me
            return False

        prev_record = cls.get_previous(record.timestamp)
        next_record = cls.get_next(record.timestamp)

        if prev_record is None and next_record is None:
            # Uh, how did you manage to do this?
            # I'm not even mad, that's amazing.
            return False

        if (
            isinstance(prev_record, NistRandomnessBeaconValue) and
            isinstance(next_record, NistRandomnessBeaconValue)
        ):
            # Majority case, somewhere in the middle of the chain
            # True if:
            #   - All three records have proper signatures
            #   - The requested record's previous output equals previous
            #   - The next possible record's previosu output equals the record
            return (
                record.valid_signature and
                prev_record.valid_signature and
                next_record.valid_signature and
                record.previous_output_value == prev_record.output_value and
                next_record.previous_output_value == record.output_value
            )

        if (
            prev_record is None and
            isinstance(next_record, NistRandomnessBeaconValue)
        ):
            # Edge case, this was potentially the first record of all time
            init_ref = NistRandomnessBeaconValue.from_json(
                cn.NIST_INIT_RECORD,
            )

            return (
                record.valid_signature and
                next_record.valid_signature and
                init_ref == record and
                next_record.previous_output_value == record.output_value
            )

        if (
            isinstance(prev_record, NistRandomnessBeaconValue) and
            next_record is None
        ):
            # Edge case, this was potentially the latest and greatest
            return (
                record.valid_signature and
                prev_record.valid_signature and
                record.previous_output_value == prev_record.output_value
            )

    @classmethod
    def get_last_record(cls) -> NistRandomnessBeaconValue:
        """
        Get the last (newest) record available.

        :return: The last beacon value. 'None' otherwise.
        """

        return cls._query_nist("last")

    @classmethod
    def get_next(cls, timestamp: int) -> NistRandomnessBeaconValue:
        """
        Given a record timestamp, get the next record available.

        :param timestamp: UNIX time / POSIX time / Epoch time
        :return: The next beacon value if available. 'None' otherwise.
        """

        return cls._query_nist("next/{}".format(timestamp))

    @classmethod
    def get_previous(cls, timestamp: int) -> NistRandomnessBeaconValue:
        """
        Given a record timestamp, get the previous record available.

        :param timestamp: UNIX time / POSIX time / Epoch time
        :return: The previous beacon value if available. 'None; otherwise
        """

        return cls._query_nist("previous/{}".format(timestamp))

    @classmethod
    def get_record(cls, timestamp: int) -> NistRandomnessBeaconValue:
        """
        Get a specific record (or next closest)

        :param timestamp: UNIX time / POSIX time / Epoch time
        :return: The requested beacon value if available. 'None' otherwise.
        """

        return cls._query_nist(str(timestamp))
