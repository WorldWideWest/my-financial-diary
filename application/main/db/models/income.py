from main.db.models.base import BaseModel

class IncomeModel(BaseModel):
    table_name = "planned-income"

    id: int = None
    month_id: int = None
    year: int = None
    planned_income: int = None

    






    
