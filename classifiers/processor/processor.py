import warnings

# from nltk.help import upenn_tagset
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from typing import Any, List

class Processor:
    def __init__(self, data: List[str], valid_word_tags: List[str], tag: str = None):
        self.data: List[str] = data
        self.valid_word_tags: List[str] = valid_word_tags
        self.tag : str = tag
        
        self.documents: List[str] = []
        self.tokenized_data: List[List[str]] = []

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

    def run(self) -> None:
        for d in self.data:
            # Tag documents
            if self.tag:
                self.documents.append(d, self.tag)

            # Tag words
            unvalidated_words: List[Any] = word_tokenize(d)
            pos: Any = pos_tag(unvalidated_words)

            # Filter in lowercase words that are associated with valid tags
            words: List[str] = []
            for p in pos:
                if p[1][0] in self.valid_word_tags:
                    words.append(p[0].lower())

            self.tokenized_data.append(words)
