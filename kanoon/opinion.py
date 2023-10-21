import csv
import re
from pypdf import PdfReader

class Opinion:
    def __init__(self, file):
        self.reader = PdfReader(file)

    def parse(self):
        self.text = self.text()
        self.citation = self.citation()
        self.forum = self.forum()
        self.case_number = self.case_number()
        self.appellants = self.appellants()
        self.respondents = self.respondents()
        self.date_decided = self.date_decided()
        self.case_note = self.casenote()

    def text(self):
        text = []
        for page in self.reader.pages:
            text.append(page.extract_text())
        text = "".join(text)
        text = re.sub("/[,]/ ","", text)
        return text 
    
    def citation(self) -> str:
        return str(re.search('^([^\s]+)', self.text).group()).strip()

    def forum(self) -> str:
        return str(re.search("(?:\r\n?|\n){2}(.+)", self.text).group()).strip()

    def case_number(self) -> str:
        return str(re.search("^(?=.*(No\.|Nos\.) ).*$", self.text).group()).strip()

    def appellants(self) -> str:
        return self._text_between('Appellants:', 'Vs.')

    def date_decided(self):
        return self._text_between('Decided On:', 'Appellants:')

    def respondents(self):
        return self._text_between('Respondent:', "Hon\'ble Judges/Coram:\n")

    def casenote(self):
        if self.has_casenote():
            casenote = self._text_between("Case Note:\n", "ORDER\n") if self.is_order() else ""
            casenote = self._text_between("Case Note:\n", "JUDGMENT\n") if self.is_judgment() else ""
        else:
          casenote = 'COULD NOT FIND CASE NOTE'

        return casenote
    
    def has_casenote(self):
        return "Case Note:\n" in self.text

    def is_judgment(self):
        return "JUDGMENT\n" in self.text

    def is_order(self):
        return "ORDER\n" in self.text

    def _text_between(self, phrase1, phrase2):
       return self.text.split(phrase1)[-1].split(phrase2)[0]

