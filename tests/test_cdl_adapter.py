# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the OpenTimelineIO project

"""Test the CDL export adapter."""

# python
import os
import shutil
import unittest
import inspect

import opentimelineio as otio

MODULE = otio.adapters.from_name('cdl').module()

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
TEMP_TESTS_OUTPUT_DIR = os.path.join(SAMPLE_DATA_DIR, "CDL_EXPORTS")
SAMPLE_CDL_EDL_PATH = os.path.join(SAMPLE_DATA_DIR, "sample_cdl_edl.edl")
SAMPLE_CDL_ALE_PATH = os.path.join(SAMPLE_DATA_DIR, "sample_cdl_ale.ale")


class CDLAdapterTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEMP_TESTS_OUTPUT_DIR):
            shutil.rmtree(TEMP_TESTS_OUTPUT_DIR)
        os.makedirs(TEMP_TESTS_OUTPUT_DIR)

    def tearDown(self):
        shutil.rmtree(TEMP_TESTS_OUTPUT_DIR)

    def test_edl_read(self):
        edl_path = SAMPLE_CDL_EDL_PATH

        timeline = otio.adapters.read_from_file(edl_path, rate=25.000)
        self.assertTrue(timeline is not None)
        self.assertEqual(type(timeline), otio.schema.Timeline)
        self.assertEqual(len(timeline.tracks[0]), 10)
        self.assertEqual(
            [c.name for c in timeline.tracks[0]],
            ["VFX_NAME_01", "VFX_NAME_02", "VFX_NAME_03", "VFX_NAME_04",
             "VFX_NAME_05", "VFX_NAME_06", "VFX_NAME_07", "VFX_NAME_08",
             "VFX_NAME_09", "VFX_NAME_10"]
        )

    def test_ale_read(self):
        ale_path = SAMPLE_CDL_ALE_PATH

        otio_collection = otio.adapters.read_from_file(ale_path)
        self.assertTrue(otio_collection is not None)
        self.assertEqual(
            type(otio_collection),
            otio.schema.SerializableCollection
        )
        self.assertEqual(len(otio_collection), 8)
        self.assertEqual(
            [c.name for c in otio_collection],
            ["SAMPLE_CLIP_01", "SAMPLE_CLIP_02", "SAMPLE_CLIP_03",
             "SAMPLE_CLIP_04", "SAMPLE_CLIP_05", "SAMPLE_CLIP_06",
             "SAMPLE_CLIP_07", "SAMPLE_CLIP_08"]
        )

    def test_write_cdl_from_edl(self):
        edl_path = SAMPLE_CDL_EDL_PATH
        otio_instance = otio.adapters.read_from_file(edl_path, rate=25.000)
        otio.adapters.write_to_file(
            otio_instance,
            TEMP_TESTS_OUTPUT_DIR,
            adapter_name='cdl'
        )

        cdl_files = [f for f in sorted(os.listdir(TEMP_TESTS_OUTPUT_DIR))]

        first_cdl_filepath = os.path.join(TEMP_TESTS_OUTPUT_DIR, cdl_files[0])
        last_cdl_filepath = os.path.join(TEMP_TESTS_OUTPUT_DIR, cdl_files[-1])
        first_cdl_file = open(first_cdl_filepath, "r")
        last_cdl_file = open(last_cdl_filepath, "r")

        cdl1 = """<?xml version="1.0" encoding="utf-8"?>
                    <ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
                        <ColorDecision>
                            <ColorCorrection id="A001C001_220201_ABCD">
                                <SOPNode>
                                    <Slope>0.912700 0.912700 0.912700</Slope>
                                    <Offset>0.024500 0.024500 0.024500</Offset>
                                    <Power>1.010000 1.120000 0.910000</Power>
                                </SOPNode>
                                <SATNode>
                                    <Saturation>1.000000</Saturation>
                                </SATNode>
                            </ColorCorrection>
                        </ColorDecision>
                    </ColorDecisionList>
                """
        cdl2 = """<?xml version="1.0" encoding="utf-8"?>
                    <ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
                        <ColorDecision>
                            <ColorCorrection id="A001C010_220201_ABCD">
                                <SOPNode>
                                    <Slope>0.832000 0.798000 0.964000</Slope>
                                    <Offset>0.042300 0.034500 0.035200</Offset>
                                    <Power>1.000000 1.000000 1.000000</Power>
                                </SOPNode>
                                <SATNode>
                                    <Saturation>0.200000</Saturation>
                                </SATNode>
                            </ColorCorrection>
                        </ColorDecision>
                    </ColorDecisionList>
                """

        self.assertEqual(len(cdl_files), 10)

        self.assertEqual(
            first_cdl_file.read().strip(),
            inspect.cleandoc(cdl1)
        )

        self.assertEqual(
            last_cdl_file.read().strip(),
            inspect.cleandoc(cdl2)
        )

        first_cdl_file.close()
        last_cdl_file.close()

    def test_write_cdl_from_ale(self):
        ale_path = SAMPLE_CDL_ALE_PATH
        otio_instance = otio.adapters.read_from_file(ale_path)
        otio.adapters.write_to_file(
            otio_instance,
            TEMP_TESTS_OUTPUT_DIR,
            adapter_name='cdl'
        )

        cdl_files = [f for f in sorted(os.listdir(TEMP_TESTS_OUTPUT_DIR))]

        first_cdl_filepath = os.path.join(TEMP_TESTS_OUTPUT_DIR, cdl_files[0])
        last_cdl_filepath = os.path.join(TEMP_TESTS_OUTPUT_DIR, cdl_files[-1])
        first_cdl_file = open(first_cdl_filepath, "r")
        last_cdl_file = open(last_cdl_filepath, "r")

        cdl1 = """<?xml version="1.0" encoding="utf-8"?>
                    <ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
                        <ColorDecision>
                            <ColorCorrection id="A001C001_220201_ABCD">
                                <SOPNode>
                                    <Slope>1.123400 1.567800 1.432100</Slope>
                                    <Offset>1.123400 1.567800 1.432100</Offset>
                                    <Power>1.123400 1.567800 1.432100</Power>
                                </SOPNode>
                                <SATNode>
                                    <Saturation>1.123000</Saturation>
                                </SATNode>
                            </ColorCorrection>
                        </ColorDecision>
                    </ColorDecisionList>
                """
        cdl2 = """<?xml version="1.0" encoding="utf-8"?>
                    <ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
                        <ColorDecision>
                            <ColorCorrection id="A001C008_220201_ABCD">
                                <SOPNode>
                                    <Slope>1.123400 1.567800 1.432100</Slope>
                                    <Offset>1.123400 1.567800 1.432100</Offset>
                                    <Power>1.123400 1.567800 1.432100</Power>
                                </SOPNode>
                                <SATNode>
                                    <Saturation>1.123000</Saturation>
                                </SATNode>
                            </ColorCorrection>
                        </ColorDecision>
                    </ColorDecisionList>
                """

        self.assertEqual(len(cdl_files), 8)

        self.assertEqual(
            first_cdl_file.read().strip(),
            inspect.cleandoc(cdl1)
        )

        self.assertEqual(
            last_cdl_file.read().strip(),
            inspect.cleandoc(cdl2)
        )

        first_cdl_file.close()
        last_cdl_file.close()


if __name__ == '__main__':
    unittest.main()
