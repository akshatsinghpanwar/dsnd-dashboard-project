import pandas as pd

from .sql_execution import QueryMixin


class QueryBase(QueryMixin):
    name = ""

    def names(self):
        return []

    def event_counts(self, id):
        query = f"""
            SELECT e.event_date,
                   SUM(e.positive_events) AS positive_events,
                   SUM(e.negative_events) AS negative_events
            FROM employee_events e
            JOIN {self.name} s USING({self.name}_id)
            WHERE s.{self.name}_id = {id}
            GROUP BY e.event_date
            ORDER BY e.event_date
        """
        return self.pandas_query(query)

    def notes(self, id):
        query = f"""
            SELECT n.note_date, n.note
            FROM notes n
            JOIN {self.name} s USING({self.name}_id)
            WHERE s.{self.name}_id = {id}
            ORDER BY n.note_date
        """
        return self.pandas_query(query)

