from helpers.constants import DEFAULT_FILES_PATH


class RagRetrievalServiceInterface:
    def get_default_file_path(self) -> str:
        return DEFAULT_FILES_PATH

    def embed_files(
        self, files_location: str | None = None, pre_delete_data=False
    ) -> None:
        pass

    def retrieve(self, query: str) -> str:
        pass
