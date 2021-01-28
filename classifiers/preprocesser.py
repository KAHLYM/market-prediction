import warnings

# from nltk.help import upenn_tagset
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from typing import Any, List

class PreProcessor:
    def __init__(self, data: List[str], valid_word_tags: List[str]):
        self.data: List[str] = data
        self.valid_word_tags: List[str] = valid_word_tags

    @property
    def valid_word_tags(self) -> List[str]:
        return self._valid_word_tags

    @valid_word_tags.setter
    def valid_word_tags(self, value: List[str]):
        if not value:
            warnings.warn('valid_word_tags will contain not tags')
        # TODO: Raise AttributeError for invalid tags
        # elif (tag not in upenn_tagset() for tag in value):
        #     raise AttributeError(f'invalid value, valid_word_tags contains an invalid tag')

        self._valid_word_tags = value

    @valid_word_tags.deleter
    def valid_word_tags(self):
        raise AttributeError('do not delete, valid_word_tags can be set emptied')

    def run(self) -> List[str]:
        # Tokenize
        tokenized_data: List[List[str]] = []
        for d in self.data:
            unvalidated_words: List[Any] = word_tokenize(d)

            # Tag words
            pos: Any = pos_tag(unvalidated_words)

            # Filter in lowercase words that are associated with valid tags
            words: List[str] = []
            for p in pos:
                if p[1][0] in self.valid_word_tags:
                    words.append(p[0].lower())

            tokenized_data.append(words)

        return tokenized_data
