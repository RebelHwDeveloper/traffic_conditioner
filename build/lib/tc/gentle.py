import shlex
import subprocess

from tc import Degrade, Command


class Gentle(Degrade):
    """

    """

    # def eliminate_old_config(interface):
    #     super(Gentle, self).eliminate_old_config(interface)

    @property
    def reorder(self) -> bool:
        """This is the property that holds the value for the reordering rate of the 'gentle' profile.

            In this profile it is not necessary to specify the reordering because we assume a linearly equivalent
            network so that no packet can have rerouting with different paths, which means pahse-velocity of the packet
            train is constant with respect to the network.

            Other Parameters
            ----------
            reorder : bool, optional
                If the network will reorder randomly packets
        """
        return bool(self._parser['Gentle']['Reorder'])

    @property
    def duplicate(self) -> dict:
        """This is the property that holds the value for the duplicate rate of the 'gentle' profile.

            In this profile it is not necessary to specify the duplication rate or correlation because this is a good
            equivalent channel environment, like an optical fiber or another good quality medium, with gentle neighbors
            that will not resend back again packets with big latencies.

            Other Parameters
            ----------
            probability : int, optional
                The probability of duplication of a packet
            correlation : int, optional
                The correlation of duplication with previous packets
        """
        return {
            'probability': float(self._parser['Gentle']['DuplicateChance']),
            'correlation': float(self._parser['Gentle']['DuplicateCorrelation']),
        }

    def add_root_bucket(self):
        """Helper method to add he main hook once the old configuration is wiped out"""
        stringa = "tc qdisc del dev " + self.__interface + " root"
        cmd = shlex.split(stringa)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            o, e = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise RuntimeWarning("Old configuration not eliminated")

        if e.decode('ascii') != "":
            raise RuntimeError(e.decode('ascii'))
        return str(proc.returncode)

    def make_command(self):
        """
        Method that constructs the string to be executed, this is the core of the whole module, here I will build the
        string to be executed by the system in a shell.
        Hypotheses:
            1. The system has CAP_NET_LINK privileges
            2. The old configration has been wiped out
        After add root bucket you have the main hook to put your degrader or rate limiter
        """
        # self.add_root_bucket()

        stringa = "tc qdisc add dev " + self.__interface + " root netem "
        stringa += "delay " + self.latency['latency'] + "ms " + self.latency['jitter'] + "ms " + self.latency[
            'correlation'] + "% distribution " + self.latency['distribution']
        stringa += " loss " + self.drop['probability'].__str__() + "% " + self.drop['correlation'].__str__() + "%"
        stringa += " corrupt " + self.corrupt['probability'].__str__() + "% duplicate " + \
                   self.duplicate['probability'].__str__() + "%"

        cmd = shlex.split(stringa)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            o, e = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise RuntimeWarning("Old configuration not eliminated")

        if e.decode('ascii') != "":
            raise RuntimeError(e.decode('ascii'))
        return str(proc.returncode)

    def __init__(self, config_parser, interface):
        self.__interface = interface
        super(Gentle, self).__init__(self.__interface)
        self._parser = config_parser

    @property
    def corrupt(self):
        """This is the property that holds the value for the corruption rate of the 'gentle' profile.

            In this profile it is not necessary to specify the corruption rate or correlation because this is a good channel
            environment, like an optical fiber or another good quality medium.

            Other Parameters
            ----------
            probability : int, optional
                The probability of corruption of a packet
            correlation : int, optional
                The correlation of corruption with previous packets
        """
        return {
            'probability': float(self._parser['Gentle']['CorruptProbability']),
            'correlation': float(self._parser['Gentle']['CorruptCorrelation']),
        }

    @property
    def latency(self):
        """This is the property that holds the value for the one-way latency of the 'gentle' profile.

            This is a mandatory parameter because if you don't have latency then you win a nobel prize for defeating
            Einstein. With latency we can specify the distribution. In this case I assumed a Gaussian PDF which means I
            know that the vast majority of the latency experienced by my packets will be something around mean value.

            Other Parameters
            ----------
            latency : int
                One-way latency of the packet
            jitter : int, optional
                Variance of the of the latency
            distribution : str
                Type of PDF assumed, if not provided uniform will be assumed
            correlation : int, optional
                How much is correlated with the value of the previous packets
        """
        return {
            'latency': self._parser.get('Gentle', 'LatencyMean'),
            'jitter': self._parser.get('Gentle', 'LatencyVariance'),
            'distribution': self._parser.get('Gentle', 'LatencyDistribution'),
            'correlation': self._parser.get('Gentle', 'LatencyCorrelation'),
        }

    @property
    def drop(self):
        """This is the property that holds the value for the one-way latency of the 'gentle' profile.

            This value represents the drop model for the traffic conditioner. In this particular profile we don't have
            big values of drop probability, because it's a gentle situation. I neglect every network saturation effect
            so in this model it is not possible to simulate AQM mechanism such as RED or other variants.

            Other Parameters
            ----------
            probability : int, optional
                Drop probability
            correlation : int, optional
                How much is correlated with the value of the previous packets
        """
        return {
            'probability': float(self._parser['Gentle']['DropProbability']),
            'correlation': float(self._parser['Gentle']['DropCorrelation']),
        }


class GentleCommand(Command):

    def __init__(self, profile: Gentle):
        self._profile = profile

    def execute(self):
        self._profile.make_command()
