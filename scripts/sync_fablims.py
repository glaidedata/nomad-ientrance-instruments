import json
import os
import time

import requests


def sync_fablims_to_nomad(output_dir='nomad_upload'):
    """Fetches data from FabLIMS API and prepares NOMAD archives."""

    # 1. API Configuration
    base_url = 'https://ientrance.fablims.com/api/equipments'

    # Fetch the API key from your computer's environment variables
    api_key = os.getenv('FABLIMS_API_KEY')
    if not api_key:
        raise ValueError(
            'ERROR: Please set the FABLIMS_API_KEY environment variable before running this script.'
        )

    headers = {'x-api-key': api_key, 'content-type': 'application/json'}

    os.makedirs(output_dir, exist_ok=True)
    limit = 50
    skip = 0
    total_processed = 0

    print('Starting automated extraction from FabLIMS...')

    # 2. Fetch Data from API (Pagination Loop)
    while True:
        filter_param = f'{{"limit":{limit},"skip":{skip},"order":["id asc"]}}'
        response = requests.get(
            f'{base_url}/catalog-equipment2',
            headers=headers,
            params={'filter': filter_param},
        )

        SUCCESS_STATUS_CODES = 200
        if response.status_code != SUCCESS_STATUS_CODES:
            print(f'Error fetching data! Status: {response.status_code}')
            break

        data = response.json()
        if len(data) == 0:
            break  # Reached the end

        # 3. Process Each Instrument
        for item in data:
            instrument_id = item.get('id')

            # Extract Image
            image_filename = None
            img_obj = item.get('overviewJpgImage')
            if img_obj and isinstance(img_obj, dict) and 'data' in img_obj:
                image_filename = f'instrument_{instrument_id}_image.jpg'
                with open(os.path.join(output_dir, image_filename), 'wb') as img_file:
                    img_file.write(bytes(img_obj['data']))

            # Map Techniques
            techniques = []
            if item.get('equipmentTechniques'):
                for tech in item.get('equipmentTechniques'):
                    techniques.append(
                        {
                            'technique_id': tech.get('id'),
                            'name': tech.get('name'),
                            'generic_equipment_name': tech.get('genericEquipmentName'),
                            'main_category': tech.get('mainCategory'),
                            'sub_category': tech.get('subCategory'),
                        }
                    )

            # Map Managers
            mapped_managers = []
            managers = item.get('equipmentManagers')
            if managers and isinstance(managers, list):
                for mgr in managers:
                    mapped_managers.append(
                        {
                            'manager_id': mgr.get('id'),
                            'firstname': mgr.get('firstname'),
                            'lastname': mgr.get('lastname'),
                            'email': mgr.get('email'),
                        }
                    )

            # Format the description to include the image inline using Markdown
            desc = item.get('description', '')
            if image_filename:
                desc = f'![Instrument Image]({image_filename})\n\n' + (desc or '')

            # Build Archive
            archive = {
                'data': {
                    'm_def': 'ientrance_instruments.schema_packages.schema_package.IEntranceInstrument',
                    'name': item.get('name'),
                    'description': desc,
                    'lab_id': str(instrument_id),
                    'tenant_id': item.get('tenantId'),
                    'tenant_name': item.get('tenantName'),
                    'description_html': item.get('descriptionHtml'),
                    'manufacturer': item.get('manufacturer'),
                    'product_model': item.get('productModel'),
                    'product_serial_number': item.get('productSerialNumber'),
                    'laboratory_inventory_code': str(
                        item.get('laboratoryInventoryCode')
                    )
                    if item.get('laboratoryInventoryCode') is not None
                    else None,
                    'equipment_status_id': item.get('equipmentStatusId'),
                    'equipment_status': item.get('equipmentStatus'),
                    'public_view_is_enabled': item.get('publicViewIsEnabled'),
                    'equipment_access_policy_name': item.get(
                        'equipmentAccessPolicyName'
                    ),
                    'equipment_funding_name': item.get('equipmentFundingName'),
                    'equipment_main_contact_info': item.get('equipmentMainContactInfo'),
                    'equipment_laboratory_id': item.get('equipmentLaboratoryId'),
                    'equipment_laboratory_name': item.get('equipmentLaboratoryName'),
                    'equipment_laboratory_has_building_room_id': item.get(
                        'equipmentLaboratoryHasBuildingRoomId'
                    ),
                    'equipment_laboratory_has_building_room_name': item.get(
                        'equipmentLaboratoryHasBuildingRoomName'
                    ),
                    'building_room_name': item.get('buildingRoomName'),
                    'building_room_controlled_entrance_id': str(
                        item.get('buildingRoomControlledEntranceId')
                    )
                    if item.get('buildingRoomControlledEntranceId') is not None
                    else None,
                    'building_floor_name': item.get('buildingFloorName'),
                    'building_name': item.get('buildingName'),
                    'techniques': techniques,
                    'managers': mapped_managers,
                }
            }

            if image_filename:
                archive['data']['overview_image'] = image_filename

            # Save Archive
            with open(
                os.path.join(output_dir, f'instrument_{instrument_id}.archive.json'),
                'w',
                encoding='utf-8',
            ) as out_f:
                json.dump(archive, out_f, indent=4)

            total_processed += 1

        skip += limit
        time.sleep(0.2)  # Polite delay for the API

    print(
        f"Successfully processed {total_processed} instruments into the '{output_dir}' folder."
    )


if __name__ == '__main__':
    sync_fablims_to_nomad()
