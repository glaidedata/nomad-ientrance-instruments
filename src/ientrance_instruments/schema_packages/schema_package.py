from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad.config import config
from nomad.datamodel.metainfo.eln import ELNInstrument
from nomad.metainfo import Quantity, SubSection, Section, SchemaPackage

configuration = config.get_plugin_entry_point(
    'ientrance_instruments.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class EquipmentTechnique(Section):
    """Subsection for techniques supported by the instrument."""
    technique_id = Quantity(type=int)
    name = Quantity(type=str)
    generic_equipment_name = Quantity(type=str)
    main_category = Quantity(type=str)
    sub_category = Quantity(type=str)


class EquipmentManager(Section):
    """Subsection for equipment manager contact info."""
    manager_id = Quantity(type=int)
    firstname = Quantity(type=str)
    lastname = Quantity(type=str)
    email = Quantity(type=str)


class IEntranceInstrument(ELNInstrument):
    """
    Custom instrument schema for iEntrance.
    Inherits name, description, datetime, tags, and the instrument_identifiers
    subsection from ELNInstrument.
    """
    m_def = Section(
        label='iEntrance Instrument',
        a_eln=dict(lane_width='600px')
    )

    # --- Core iEntrance/FabLIMS Fields ---
    fablims_id = Quantity(
        type=int,
        description='Persistent ID from FabLIMS.',
        a_eln=dict(component='NumberEditQuantity')
    )
    tenant_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    tenant_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    description_html = Quantity(type=str, a_eln=dict(component='RichTextEditQuantity'))
    manufacturer = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    product_model = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    product_serial_number = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    laboratory_inventory_code = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))

    # --- Status & Access ---
    equipment_status_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    equipment_status = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    public_view_is_enabled = Quantity(type=bool, a_eln=dict(component='BoolEditQuantity'))
    equipment_access_policy_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    equipment_funding_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    equipment_main_contact_info = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))

    # --- Image Reference ---
    overview_image = Quantity(
        type=str,
        description='Path to the extracted JPG image of the instrument.',
        a_eln=dict(component='FileEditQuantity')
    )

    # --- Extended Location Data ---
    equipment_laboratory_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    equipment_laboratory_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    equipment_laboratory_has_building_room_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    equipment_laboratory_has_building_room_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_room_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_room_controlled_entrance_id = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_floor_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))

    # Nested subsections
    managers = SubSection(section_def=EquipmentManager, repeats=True)
    techniques = SubSection(section_def=EquipmentTechnique, repeats=True)


m_package.__init_metainfo__()