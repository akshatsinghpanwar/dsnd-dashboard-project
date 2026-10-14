from .query_base import QueryBase


class Employee(QueryBase):
    name = 'employee'

    def names(self):
        query = """
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee
            ORDER BY employee_id
        """
        return self.query(query)

    def username(self, id):
        query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return self.query(query)

    def model_data(self, id):
        sql_query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee
            JOIN employee_events USING(employee_id)
            WHERE employee.employee_id = {id}
        """
        return self.pandas_query(sql_query)