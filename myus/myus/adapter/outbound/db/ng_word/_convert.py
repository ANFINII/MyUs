from myus.db.models.master import NgWord
from myus.domain.ng_word.data import NgWordData


def convert_data(obj: NgWord) -> NgWordData:
    return NgWordData(id=obj.id, word=obj.word)
