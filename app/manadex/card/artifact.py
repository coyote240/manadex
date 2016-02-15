from card import Castable, CardType
from creature import Creature
from enchantment import Enchantment


@CardType('artifact')
class Artifact(Castable):
    pass


@CardType('artifact', 'creature')
class ArtifactCreature(Creature, Artifact):
    pass


@CardType('artifact', 'enchantment')
class ArtifactEnchantment(Enchantment, Artifact):
    pass
