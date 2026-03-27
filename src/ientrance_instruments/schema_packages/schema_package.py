from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from nomad.config import config
from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.basesections import Instrument
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

configuration = config.get_plugin_entry_point(
    'ientrance_instruments.schema_packages:ientrance_instruments_schema_package'
)

m_package = SchemaPackage()


class EquipmentTechnique(ArchiveSection):
    """Subsection for techniques supported by the instrument."""

    technique_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    generic_equipment_name = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    main_category = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    sub_category = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))


class EquipmentManager(ArchiveSection):
    """Subsection for equipment manager contact info."""

    manager_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    firstname = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    lastname = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    email = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))


class IEntranceInstrument(Instrument):
    """
    Custom instrument schema for iEntrance.
    Inherits basic entity fields (like name and description) from Instrument.
    """

    m_def = Section(label='iEntrance Instrument', a_eln=dict(lane_width='600px'))

    # --- Core iEntrance/FabLIMS Fields ---
    tenant_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    tenant_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    description_html = Quantity(type=str, a_eln=dict(component='RichTextEditQuantity'))
    manufacturer = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    product_model = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    product_serial_number = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    laboratory_inventory_code = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )

    # --- Status & Access ---
    equipment_status_id = Quantity(type=int, a_eln=dict(component='NumberEditQuantity'))
    equipment_status = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    public_view_is_enabled = Quantity(
        type=bool, a_eln=dict(component='BoolEditQuantity')
    )
    equipment_access_policy_name = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    equipment_funding_name = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    equipment_main_contact_info = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )

    # --- Image Reference ---
    overview_image = Quantity(
        type=str,
        description='Path to the extracted JPG image of the instrument.',
        a_eln=dict(component='FileEditQuantity'),
    )

    # --- Extended Location Data ---
    equipment_laboratory_id = Quantity(
        type=int, a_eln=dict(component='NumberEditQuantity')
    )
    equipment_laboratory_name = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    equipment_laboratory_has_building_room_id = Quantity(
        type=int, a_eln=dict(component='NumberEditQuantity')
    )
    equipment_laboratory_has_building_room_name = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    building_room_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_room_controlled_entrance_id = Quantity(
        type=str, a_eln=dict(component='StringEditQuantity')
    )
    building_floor_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))
    building_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))

    # Nested subsections
    managers = SubSection(section_def=EquipmentManager, repeats=True)
    techniques = SubSection(section_def=EquipmentTechnique, repeats=True)


m_package.__init_metainfo__()
