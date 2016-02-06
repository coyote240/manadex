import card


class Artifact(card.Castable):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') in ['artifact', 'legendary artifact']


class ArtifactCreature(Artifact):

    @classmethod
    def match(cls, card_dict):
        return card_dict.get('type') == 'artifact creature'
