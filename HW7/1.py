"""
SOLID (principles of develpment)

1. Single Responsibility
    - actor

2. Open/Closed
    - extend the class

3. Liskov Substitution

4. Interface Segregation

5. Dependency Inversion
"""

import abc


class Client(abc.ABC):
    @abc.abstractmethod
    def get_complition(self) -> str:
        """..."""


class OpenAIClient(Client):
    def get_complition(self):
        return 12


class FakeOpenAIClient(Client):
    pass


# def get_complition(self):
#     return ...


def main(client: Client):
    response: str = client.get_complition()
    save_to_database(response)


main()

