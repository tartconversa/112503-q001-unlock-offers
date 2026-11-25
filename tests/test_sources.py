"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'trial.csv': ['wave', 'stratum', 'starts', 'ends', 'watch_days', 'refund_days', 'ad_quota', 'balance_quota'], 'identity.csv': ['account', 'subject', 'start', 'stop', 'src_rev'], 'episode_map.csv': ['edition', 'episode', 'canonical', 'coverage', 'src_rev'], 'assignments.csv': ['assignment', 'wave', 'stratum', 'account', 'offer', 'at'], 'observations.csv': ['observation', 'assignment', 'edition', 'episode', 'kind', 'at', 'entitlement'], 'entitlements.csv': ['entitlement', 'assignment', 'edition', 'episode', 'at', 'state', 'parent'], 'ledger.csv': ['entry', 'entitlement', 'kind', 'cents', 'booked_on', 'adjusts'], 'trial_actions.csv': ['action', 'wave', 'kind', 'at', 'account', 'source']}
REFERENCES = [('observations.csv', 'assignment', 'assignments.csv', 'assignment'), ('entitlements.csv', 'assignment', 'assignments.csv', 'assignment'), ('ledger.csv', 'entitlement', 'entitlements.csv', 'entitlement'), ('ledger.csv', 'adjusts', 'ledger.csv', 'entry')]
OBSERVED_VALUES = [('identity.csv', 'account', 'A2', 2), ('episode_map.csv', 'edition', 'V2', 4), ('ledger.csv', 'adjusts', 'M2', 2)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
