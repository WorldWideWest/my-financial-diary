class BaseModel(object):
    table_name: str = None

    def columns(self, *args, **kwargs):
        """
            The columns method extracts the variables defined in the class
        """

        return [column for column in dir(self) if not callable(getattr(self, column)) and not column.startswith("__")]