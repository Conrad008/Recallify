import csv
from io import StringIO
 
from models import Card

class CSVImporter:
    @staticmethod
    def import_cards(csv_content: str, deck_id: int) -> list[Card]:
        reader = csv.DictReader(StringIO(csv_content))
        imported = []
 
        for row in reader:
            front = (row.get("front") or "").strip()
            back = (row.get("back") or "").strip()
 
            if not front or not back:
                continue  
 
            card = Card(deck_id=deck_id, front_text=front, back_text=back)
            imported.append(card)
 
        return imported
 