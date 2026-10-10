import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class ConnectSupabase:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("Configure SUPABASE")

        self.client: Client = create_client(
            self.url,
            self.key
        )

    def get_client(self) -> Client:
        return self.client

    def insert(self, schema: str, table: str, data: list[dict]):
        response = (
            self.client
            .schema(schema)
            .table(table)
            .insert(data)
            .execute()
        )

        return response.data

    def select(self, schema: str, table: str, columns: str = "*"):
        response = (
            self.client
            .schema(schema)
            .table(table)
            .select(columns)
            .execute()
        )

        return response.data

    def get_max_value(self, schema: str, table:str, column: str):
        response = (
            self.client
            .schema(schema)
            .table(table)
            .select(column)
            .order(column, desc=True)
            .limit(1)
            .execute()
        )

        return response.data[0][column] if response.data else None