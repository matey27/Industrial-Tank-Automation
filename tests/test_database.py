
import unittest
import tempfile
import os

import database


class TestIndustrialDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.original_db_name = database.DB_NAME

        database.DB_NAME = os.path.join(
            self.temp_dir.name,
            "test_industrial.db"
        )

        database.initialize_database()

    def tearDown(self):
        database.DB_NAME = self.original_db_name
        self.temp_dir.cleanup()

    def test_database_is_created(self):
        self.assertTrue(os.path.exists(database.DB_NAME))

    def test_process_record_is_saved(self):
        database.save_process_record(
            level=55.5,
            pump=60,
            valve=25,
            mode="AUTO",
            alarm="NORMAL"
        )

        records = database.get_process_history()

        self.assertEqual(len(records), 1)
        self.assertAlmostEqual(
            records.iloc[0]["tank_level"],
            55.5
        )

    def test_event_is_saved(self):
        database.save_event(
            event_type="ALARM",
            description="High level detected",
            severity="WARNING"
        )

        events = database.get_event_history()

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events.iloc[0]["event_type"],
            "ALARM"
        )

    def test_multiple_process_records(self):
        for level in [40, 50, 60]:
            database.save_process_record(
                level=level,
                pump=50,
                valve=20,
                mode="MANUAL",
                alarm="NORMAL"
            )

        records = database.get_process_history()

        self.assertEqual(len(records), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
