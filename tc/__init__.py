import abc
import ifaddr as ifaddr

class Command(metaclass=abc.ABCMeta):
    """
    This is the class used in the Command pattern
    """

    @abc.abstractmethod
    def execute(self):
        pass


class Degrade(metaclass=abc.ABCMeta):
    """

    """

    def eliminate_old_config(self, interface):
        print("Removing old configuration")
        import subprocess
        cmd = ['tc' , 'qdisc', 'del', 'dev', interface, 'root']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            o, e = proc.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise RuntimeWarning("Old configuration not eliminated")

        print('Output: ' + o.decode('ascii'))
        print('Error: ' + e.decode('ascii'))
        print('code: ' + str(proc.returncode))

    def __init__(self, interface):
        iface_list = ifaddr.get_adapters()
        for adapter in iface_list:
            if interface == adapter.nice_name:
                break
        else:
            raise AttributeError("Interface NOT found")
        # self.eliminate_old_config(interface)

    @property
    @abc.abstractmethod
    def latency(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def drop(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def corrupt(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def duplicate(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def reorder(self) -> dict:
        pass

    @abc.abstractmethod
    def make_command(self):
        pass

    @abc.abstractmethod
    def reset_old_config(self):
        pass

class DegradeInvoker:
    """
    Has a reference to the Command, and can execute the method.
    Notice how the command.execute() is never directly called,
    but always through the invoker.
    The action invoked is decoupled from the action performed
    by the Receiver.
    The Invoker (self) invokes a Command (LunchCommand),
    and the Command executes the appropriate action (command.execute())
    """

    def __init__(self, command: Command):
        self._command = command

    def invoke(self):
        self._command.execute()