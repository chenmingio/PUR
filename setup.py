# create local version database

from app.models.sql_project_info_extra import create_project_volume_table, create_part_info_table, \
    create_project_info_table

if __name__ == '__main__':
    create_project_info_table()
    create_part_info_table()
    create_project_volume_table()