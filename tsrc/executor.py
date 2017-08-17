""" Helpers to run thing on multiple repos and collect errors """


import abc

from tsrc import ui
import tsrc


class ExecutorFailed(tsrc.Error):
    pass


class Actor(metaclass=abc.ABCMeta):

    @property
    def quiet(self):
        return False

    @abc.abstractproperty
    def description(self):
        pass

    @abc.abstractmethod
    def display_item(self, item):
        pass

    @abc.abstractmethod
    def process(self, _):
        pass


class SequentialExecutor():
    def __init__(self, actor):
        self.actor = actor
        self.errors = list()

    def process(self, items):
        if not items:
            return True
        ui.info_1(self.actor.description)
        self.actor.items = items
        self.errors = list()
        num_items = len(items)
        for i, item in enumerate(items):
            if not self.actor.quiet:
                ui.info_count(i, num_items, end="")
            try:
                self.actor.process(item)
            except tsrc.Error as error:
                self.errors.append((item, error))

        if self.errors:
            ui.error(self.actor.description, "failed")
            for item, error in self.errors:
                item_desc = self.actor.display_item(item)
                ui.info(ui.green, "*", " ",
                        ui.reset, ui.bold, item_desc, ": ",
                        ui.reset, error, sep="")
            raise ExecutorFailed()

        return True

    def process_one(self, item):
        try:
            self.actor.process(item)
        except tsrc.Error as error:
            self.errors.append((item, str(error)))


def run_sequence(items, actor):
    executor = SequentialExecutor(actor)
    return executor.process(items)
