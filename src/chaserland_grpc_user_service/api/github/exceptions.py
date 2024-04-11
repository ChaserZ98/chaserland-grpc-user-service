class GithubApiException(Exception):
    def __init__(self, message: str, documentation_url: str):
        self.message = message
        self.documentation_url = documentation_url
        super().__init__(f"Github API error: {message} - {documentation_url}")

    def __repr__(self) -> str:
        return f"GithubApiException(message={self.message!r}, documentation_url={self.documentation_url!r})"
