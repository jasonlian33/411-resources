import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """
        A class to manage the boxing ring.

        Attributes: 
            ring (List[Boxer]): The list of boxers inside the ring. 
        
        
    """

    def __init__(self):
        """
        Initializes the ring to a empty list of boxers.
        """
        self.ring: List[Boxer] = []

    def fight(self) -> str:
        """
        Lets two fighters fight

        Returns:
            A String on the boxer that won the fight
            
        Raises:
            ValueError if there are less than two boxers
        
        """
        logger.info("Receieved request to start the fight")

        if len(self.ring) < 2:
            logger.error("Invalid Value: The ring has less than two boxers")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        random_number = get_random()

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')

        self.clear_ring()

        logger.info(f"Succesfully retrieved winner of the fight:{winner.name}")
        return winner.name

    def clear_ring(self):
        """
        Clears the ring of the boxers

        If the ring is already cleared then it returns other calls the clear() function
        """
        logger.info("Clears the ring of the boxers")
        if not self.ring:
            return
        self.ring.clear()

    def enter_ring(self, boxer: Boxer):
        """
        Allows boxer to enter the ring

        Args:
            boxer (Boxer): The specific boxer

        Raises:
            TypeError if the boxer is not of the right type/attributes
            ValueError if the ring is full (more than two boxers)        
        
        """
        logger.info("Boxers entering the ring")
        if not isinstance(boxer, Boxer):
            logger.error("Invalid type: Boxer is not a valid Boxer instance")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.error("Invalid value: More than two boxers in the ring")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Succesfully added boxer with ID {boxer.id} to the ring.")

    def get_boxers(self) -> List[Boxer]:
        """
        Gets the boxers inside the ring

        Returns:
            self.ring: The boxers (in form of a list) inside the ring
        
        """
        logger.info("Gets the boxer inside the ring")
        if not self.ring:
            pass
        else:
            pass

        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        # Arbitrary calculations
        """
        Obtains the boxer's skills

        Args:
            boxer (Boxer): The specific boxer

        Returns:
            skill: The skill of the boxer
        
        """
        logger.info("Obtaining the boxers skills.")
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        return skill
