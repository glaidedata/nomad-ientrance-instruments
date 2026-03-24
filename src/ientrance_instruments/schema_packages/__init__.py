from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class IEntranceSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from ientrance_instruments.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = IEntranceSchemaPackageEntryPoint(
    name='IEntranceInstrumentsSchema',
    description='Schema package for iEntrance FabLIMS instruments.',
)
