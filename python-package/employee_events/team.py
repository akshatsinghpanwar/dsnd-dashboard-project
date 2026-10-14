from .query_base import QueryBase


class Team(QueryBase):
    name = 'team'

    def names(self):
        query = """
            SELECT team_name, team_id
            FROM team
            ORDER BY team_id
        """
        return self.query(query)

    def username(self, id):
        query = f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """
        return self.query(query)

    def model_data(self, id):
        sql_query = f"""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM team
                JOIN employee_events USING(team_id)
                WHERE team.team_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(sql_query)