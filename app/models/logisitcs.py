from app.models import sql_nrm, sql_logistics


class Part:
    def __init__(self, part, plant):
        # prepare project list
        self.part = part
        self.plant = plant
        # self.implements = self.get_implements(part)

    # get project_vendor_volume from NRM
    def get_project_dict_list_from_nrm(self):
        project_list = sql_nrm.get_project_list_by_part_and_plant(self.part, self.plant)
        project_dict_list = [self.get_project_dict_from_nrm(project) for project in project_list]
        return project_dict_list

    def get_project_dict_from_nrm(self, project):
        project_info = sql_nrm.get_project_data_and_info(project)
        vendor_list = sql_nrm.get_vendor_nominated_list_by_project_part(project, self.part)
        vendor_dict_list = [self.get_vendor_dict_from_nrm(project, vendor) for vendor in vendor_list]
        return {'project': project, 'project_name': project_info['project_name'], 'vendor_list': vendor_dict_list}

    def get_vendor_dict_from_nrm(self, project, vendor):
        vendor_info = sql_nrm.get_vendor_info(vendor)
        volume_dict_list = sql_logistics.build_volumes_object_for_nrm_vendor(project, self.part, vendor)
        return {'vendor': vendor, 'vendor_name': vendor_info['vendor_name'], 'volumes': volume_dict_list}

    def get_delivery(self, vendor):
        return sql_logistics.get_delivery(self.part, vendor)


