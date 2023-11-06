import toml
from urllib import request
from project import Project


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        toml_content = toml.loads(content)['tool']['poetry']

        name = toml_content ['name']

        description = toml_content['description']

        license = toml_content['license']

        authors = toml_content['authors']

        dependencies = [a for a in toml_content['dependencies'].keys()]

        dev_dependencies = [a for a in toml_content['group']['dev']['dependencies']]

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(name, description, license, authors, dependencies, dev_dependencies)
