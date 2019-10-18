from tc import Degrade, Command


class Aggressive(Degrade):
    @property
    def rate(self) -> dict:
        pass

    @property
    def reorder(self) -> bool:
        """This is the property that holds the value for the reordering rate of the 'aggressive' profile.

            In this profile it is necessary to specify the reordering because we don't assume a linearly equivalent
            network so that packet can have rerouting with different paths, we assume packets cab take panoramic routes.

            Other Parameters
            ----------
            reorder : bool
                If the network will reorder randomly packets
        """
        return bool(self._parser['Aggressive']['Reorder'])

    @property
    def duplicate(self) -> dict:
        """This is the property that holds the value for the duplicate rate of the 'aggressive' profile.

            In this profile it is necessary to specify the duplication rate or correlation because this is a bad
            equivalent channel environment, like a WiFi or another bad quality medium, with aggressive neighbors
            that will resend back again packets with big latencies at random times.

            Other Parameters
            ----------
            probability : int
                The probability of duplication of a packet
            correlation : int, optional
                The correlation of duplication with previous packets
        """
        return {
            'probability': float(self._parser['Aggressive']['DuplicateChance']),
            'correlation': float(self._parser['Aggressive']['DuplicateCorrelation']),
        }

    def make_command(self):
        """
        Method that constructs the string to be executed
        :rtype: str
        """
        stringa = "Constructing execution string"
        print(stringa)
        return stringa

    def __init__(self, config_parser, interface):
        super(Aggressive, self).__init__(interface='eth0')
        self._parser = config_parser

    @property
    def corrupt(self):
        """This is the property that holds the value for the corruption rate of the 'aggressive' profile.

            In this profile it is necessary to specify the corruption rate or correlation because this is a bad channel
            environment, like an WiFi or another bad environment which can corrupt packets. With respect to noise and
            channel modeling, Netem provides some interesting models like the Gilbert-Elliot which assumes a 4 state
            Markov Chain for error coding control and transmission errors. In this module we will assume a 1-state
            transition matrix so that everything collapses to a Bernoullian process with just one (scalar) parameter.

            Other Parameters
            ----------
            probability : int
                The probability of corruption of a packet (Bernoullian model)
            correlation : int, optional
                The correlation of corruption with previous packets
        """
        return {
            'probability': float(self._parser['Aggressive']['CorruptProbability']),
            'correlation': float(self._parser['Aggressive']['CorruptCorrelation']),
        }

    @property
    def latency(self):
        """This is the property that holds the value for the one-way latency of the 'aggressive' profile.

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
            'latency': self._parser.get('Aggressive', 'LatencyMean'),
            'jitter': self._parser.get('Aggressive', 'LatencyVariance'),
            'distribution': self._parser.get('Aggressive', 'LatencyDistribution'),
            'correlation': self._parser.get('Aggressive', 'LatencyCorrelation'),
        }

    @property
    def drop(self):
        """This is the property that holds the value for the one-way latency of the 'aggressive' profile.

            This value represents the drop model for the traffic conditioner. In this particular profile we don't have
            big values of drop probability, because it's a aggressive situation. I neglect every network saturation
            effect so in this model it is not possible to simulate AQM mechanism such as RED or other variants.

            Other Parameters
            ----------
            probability : int, optional
                Drop probability
            correlation : int, optional
                How much is correlated with the value of the previous packets
        """
        return {
            'probability': float(self._parser['Aggressive']['DropProbability']),
            'correlation': float(self._parser['Aggressive']['DropCorrelation']),
        }


class AggressiveCommand(Command):

    def __init__(self, profile: Aggressive):
        self._profile = profile

    def execute(self):
        'Qui ci metto la mia stringa precisa tc qdisc ....'
        self._profile.make_command()
