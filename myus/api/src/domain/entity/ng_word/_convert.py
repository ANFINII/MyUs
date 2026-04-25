from api.db.models.master import NgWord
from api.src.domain.interface.ng_word.data import NgWordData


def convert_data(obj: NgWord) -> NgWordData:
    return NgWordData(id=obj.id, word=obj.word)
