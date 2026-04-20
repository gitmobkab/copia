import faker


_fake = faker.Faker()
"""global faker instance for all generators based on faker"""

def get_faker() -> faker.Faker:
    """return the global faker object"""
    return _fake

# TODO: implement a set_locale function to update the global faker locale dynamically
