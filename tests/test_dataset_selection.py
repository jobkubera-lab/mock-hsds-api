import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app


class DatasetSelectionTests(unittest.TestCase):
    def setUp(self):
        self.original_data_root = app.DATA_ROOT
        self.original_dataset_name = app.DATASET_NAME

    def tearDown(self):
        app.DATA_ROOT = self.original_data_root
        app.DATASET_NAME = self.original_dataset_name

    def test_uses_legacy_data_root_when_no_dataset_is_selected(self):
        with tempfile.TemporaryDirectory() as directory:
            app.DATA_ROOT = Path(directory)
            app.DATASET_NAME = None

            self.assertEqual(app.get_data_directory(), Path(directory))

    def test_uses_named_dataset_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            data_root = Path(directory)
            dataset = data_root / "all-valid-data"
            dataset.mkdir()

            app.DATA_ROOT = data_root
            app.DATASET_NAME = "all-valid-data"

            self.assertEqual(app.get_data_directory(), dataset.resolve())

    def test_missing_named_dataset_fails_clearly(self):
        with tempfile.TemporaryDirectory() as directory:
            app.DATA_ROOT = Path(directory)
            app.DATASET_NAME = "missing-dataset"

            with self.assertRaisesRegex(FileNotFoundError, "missing-dataset"):
                app.get_data_directory()

    def test_rejects_dataset_outside_data_root(self):
        with tempfile.TemporaryDirectory() as directory:
            app.DATA_ROOT = Path(directory) / "data"
            app.DATA_ROOT.mkdir()
            app.DATASET_NAME = "../../etc"

            with self.assertRaisesRegex(ValueError, "outside data root"):
                app.get_data_directory()

    def test_parse_args_accepts_dataset_option(self):
        with patch("sys.argv", ["app.py", "--dataset", "mixed-data"]):
            args = app.parse_args()

        self.assertEqual(args.dataset, "mixed-data")

    def test_environment_variable_configures_dataset_on_import(self):
        with patch.dict(os.environ, {"HSDS_DATASET": "all-valid-data"}):
            importlib.reload(app)
            self.assertEqual(app.DATASET_NAME, "all-valid-data")

        importlib.reload(app)


if __name__ == "__main__":
    unittest.main()
