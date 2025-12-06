import unittest
import json
import os

class TestPhilippineRegions(unittest.TestCase):
    FILENAME = 'ph_updated_nir.json'

    @classmethod
    def setUpClass(cls):
        """Load the JSON file once before running tests."""
        if not os.path.exists(cls.FILENAME):
            raise FileNotFoundError(f"Could not find {cls.FILENAME}")
        
        with open(cls.FILENAME, 'r', encoding='utf-8') as f:
            cls.geojson_data = json.load(f)
            cls.features = cls.geojson_data['features']

    def test_total_region_count(self):
        """Test #1: The file should have exactly 18 administrative regions."""
        count = len(self.features)
        self.assertEqual(count, 18, f"Expected 18 regions, but found {count}")

    def test_nir_existence(self):
        """Test #2: 'Negros Island Region' should exist in the properties."""
        region_names = [f['properties']['name'] for f in self.features]
        self.assertIn("Negros Island Region", region_names, "Negros Island Region was not found in the file.")

    def test_nir_structure_and_id(self):
        """Test #3: NIR should have the correct ID (PH18) and valid geometry."""
        # Find the NIR feature object
        nir_feature = next((f for f in self.features if f['properties']['name'] == "Negros Island Region"), None)
        
        # Check if found (redundant to Test #2 but necessary for variable assignment)
        self.assertIsNotNone(nir_feature, "Could not retrieve NIR feature object.")
        
        # Check ID
        self.assertEqual(nir_feature['properties']['id'], "PH18", "NIR should have the ID 'PH18'.")
        
        # Check Geometry Type
        self.assertEqual(nir_feature['geometry']['type'], "MultiPolygon", "NIR geometry type should be 'MultiPolygon'.")
        
        # Check that coordinates are not empty (it actually has land shape)
        self.assertTrue(len(nir_feature['geometry']['coordinates']) > 0, "NIR feature has no coordinates/geometry data.")

    def test_source_regions_integrity(self):
        """Test #4: Western Visayas (PH06) and Central Visayas (PH07) should still exist."""
        # Even though we split them, the original region entries should remain for the non-Negros provinces
        region_ids = [f['properties']['id'] for f in self.features]
        
        self.assertIn("PH06", region_ids, "Western Visayas (PH06) is missing.")
        self.assertIn("PH07", region_ids, "Central Visayas (PH07) is missing.")

if __name__ == '__main__':
    print(f"Running tests on: {TestPhilippineRegions.FILENAME}")
    unittest.main(verbosity=2)