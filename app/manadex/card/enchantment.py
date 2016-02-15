from card import Castable, CardType
from creature import Creature


@CardType('enchantment')
class Enchantment(Castable):
    pass


@CardType('enchantment', 'creature')
class EnchantmentCreature(Creature, Enchantment):
    pass
