import card
from creature import Creature
from enchantment import Enchantment


class Artifact(card.Castable):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'artifact'


class ArtifactCreature(Creature, Artifact):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'artifact creature'


class ArtifactEnchantment(Enchantment, Artifact):

    @classmethod
    def match(cls, card_dict):
        return set(('artifact', 'creature')) in set(card_dict.get('types'))
