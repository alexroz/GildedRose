from abc import ABC, abstractmethod

from item import Item

class ItemHandler(ABC):
    """
    Base for item handlers that calculate item updates
    """    
    @abstractmethod
    def can_handle(self, item: Item) -> bool:
        """
        Indicates whether this handle can process this kind of item
        """
        raise NotImplementedError()

    @abstractmethod
    def update_quality(self, item: Item):
        """
        Updates item sell in and quality for 1 day
        """
        raise NotImplementedError()

    @property
    def quality_decay_factor(self) -> int:
        """
        The base multiplier for item quality calculations
        """
        return 1