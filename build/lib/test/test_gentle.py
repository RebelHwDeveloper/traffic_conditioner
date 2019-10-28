from unittest import TestCase
from configparser import ConfigParser

import patch as patch

from tc.gentle import Gentle

interface = "ens33"
config = ConfigParser()


class TestGentle(TestCase):
    def setUp(self) -> None:
        import os
        config.read(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.ini')))

    def test_reorder(self):
        profile = Gentle(config, interface)
        self.assertEqual(profile.reorder, bool(config['Gentle']['Reorder']))

    def test_duplicate(self):
        profile = Gentle(config, interface)
        self.assertEqual(profile.duplicate, {'probability': float(config['Gentle']['DuplicateChance']),
                                             'correlation': float(config['Gentle']['DuplicateCorrelation'])})

    def test_corrupt(self):
        profile = Gentle(config, interface)
        self.assertEqual(profile.corrupt, {'probability': float(config['Gentle']['CorruptProbability']),
                                           'correlation': float(config['Gentle']['CorruptCorrelation'])})

    def test_latency(self):
        profile = Gentle(config, interface)
        self.assertEqual(profile.latency, {'latency': config['Gentle']['LatencyMean'],
                                           'jitter': config['Gentle']['LatencyVariance'],
                                           'distribution': config['Gentle']['LatencyDistribution'],
                                           'correlation': config['Gentle']['LatencyCorrelation']
                                           })

    def test_drop(self):
        profile = Gentle(config, interface)
        self.assertEqual(profile.drop, {'correlation': float(config['Gentle']['DropCorrelation']),
                                        'probability': float(config['Gentle']['DropProbability'])})

    def test___init__(self):
        self.assertRaises(AttributeError, Gentle, config, interface="eth0")

    def test_eliminate_old(self):
        # Test when interface is not
        # right if put with other test it will break them
        # Casino da testare
        self.assertRaises(AttributeError, Gentle, config, interface="eth0")

    def test_make_command(self):
        obj = Gentle(config, "ens33")
        self.assertEqual(obj.make_command(),
                         "tc qdisc add dev ens33 root netem delay 40ms 5ms 5% "
                         "distribution normal loss 3.0% 25.0% corrupt 0.01% duplicate 0.001%")

    def test_add_root_bucket(self):
        obj = Gentle(config, "ens33")
        self.assertEqual(obj.add_root_bucket(),
                         "tc qdisc del dev ens33 root")
