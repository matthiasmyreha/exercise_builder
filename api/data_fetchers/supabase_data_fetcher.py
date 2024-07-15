from model.data_fetcher import DataFetcher


class SupabaseDataFetcher(DataFetcher):
    def fetchPhonemes(self) -> str:
        print("fetch Phonemes from Supabase")

    def fetchCategories(self) -> str:
        print("fetch Categories from Supabase")

    def fetchItems(self) -> str:
        print("fetch Items from Supabase")
