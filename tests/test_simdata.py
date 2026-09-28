import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIMDATA = ROOT / "simdata"
TUNING = ROOT / "tuning"


class BuffSimDataTests(unittest.TestCase):
    def test_every_outcome_buff_has_matching_ui_simdata(self):
        tuning_files = sorted(TUNING.glob("ValeriesJobs_Buff_*.xml"))
        simdata_files = sorted(SIMDATA.glob("ValeriesJobs_Buff_*.xml"))
        self.assertEqual([path.name for path in simdata_files], [path.name for path in tuning_files])

        for tuning_path in tuning_files:
            with self.subTest(path=tuning_path.name):
                tuning = ET.parse(tuning_path).getroot()
                simdata = ET.parse(SIMDATA / tuning_path.name).getroot()
                instance = simdata.find("./Instances/I")
                self.assertEqual(simdata.attrib["version"], "0x00000101")
                self.assertEqual(simdata.attrib["u"], "0x80000000")
                self.assertEqual(instance.attrib["name"], tuning.attrib["n"])

                fields = {
                    field.attrib["name"]: field.text or ""
                    for field in instance.findall("./T")
                }
                self.assertEqual(fields["buff_name"].lower(), tuning.find("./T[@n='buff_name']").text.lower())
                self.assertEqual(
                    fields["buff_description"].lower(),
                    tuning.find("./T[@n='buff_description']").text.lower(),
                )
                self.assertEqual(fields["mood_type"], tuning.find("./T[@n='mood_type']").text)
                self.assertEqual(fields["mood_weight"], tuning.find("./T[@n='mood_weight']").text)

    def test_builder_packages_buff_simdata(self):
        builder = (ROOT / "tools" / "build_package.js").read_text()
        self.assertIn("SimDataResource.fromXml", builder)
        self.assertIn("group: SimDataGroup.Buff", builder)
        for path in SIMDATA.glob("ValeriesJobs_Buff_*.xml"):
            self.assertIn(path.name, builder)


if __name__ == "__main__":
    unittest.main()
