from abc import ABC, abstractmethod


class Module(ABC):
    @abstractmethod
    def run(self, img, **kwargs):
        pass

    @abstractmethod
    def draw(self, img, **kwargs):
        pass

    @abstractmethod
    def destroy(self, **kwargs):
        pass

    @abstractmethod
    def get_module_name(self):
        pass
