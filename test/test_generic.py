import shlex
import subprocess
from unittest import TestCase
from configparser import ConfigParser

from tc.generic import Generic

interface = "ens33"
config = ConfigParser()
key="Gentle"

class TestGeneric(TestCase):
    def setUp(self) -> None:
        import os
        config.read(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.ini')))

    def test_reorder(self):
        profile = Generic(config, interface, key)
        self.assertEqual(profile.reorder, bool(config['Gentle']['Reorder']))

    def test_duplicate(self):
        profile = Generic(config, interface, key)
        self.assertEqual(profile.duplicate, {'probability': float(config['Gentle']['DuplicateChance']),
                                             'correlation': float(config['Gentle']['DuplicateCorrelation'])})

    def test_corrupt(self):
        profile = Generic(config, interface, key)
        self.assertEqual(profile.corrupt, {'probability': float(config['Gentle']['CorruptProbability']),
                                           'correlation': float(config['Gentle']['CorruptCorrelation'])})

    def test_latency(self):
        profile = Generic(config, interface, key)
        self.assertEqual(profile.latency, {'latency': config['Gentle']['LatencyMean'],
                                           'jitter': config['Gentle']['LatencyVariance'],
                                           'distribution': config['Gentle']['LatencyDistribution'],
                                           'correlation': config['Gentle']['LatencyCorrelation']
                                           })

    def test_drop(self):
        profile = Generic(config, interface, key)
        self.assertEqual(profile.drop, {'correlation': float(config['Gentle']['DropCorrelation']),
                                        'probability': float(config['Gentle']['DropProbability'])})

    def test___init__(self):
        self.assertRaises(AttributeError, Generic, config, interface="eth0", key=key)

    def test_make_command(self):
        obj = Generic(config, interface, key)
        self.assertEqual(obj.make_command(), str(0))

    def test_reset_old_config(self):
        """This test is idempotent I can run it how many times i want it
            I simply put a new qdisc and the system will erase it"""
        obj = Generic(config, interface, key)
        stringa = "tc qdisc add dev " + interface + " root netem delay 200ms"
        cmd = shlex.split(stringa)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            o, e = proc.communicate(timeout=1)
        except:
            pass
        self.assertEqual(obj.reset_old_config(), 0)
        # self.assertRaises(RuntimeWarning, "RTNETLINK answers: File exists")
