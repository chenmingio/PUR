import sqlite3


conn = sqlite3.connect('nr.db', check_same_thread=False)

def dict_factory_single(cursor, row):
    d = {}
    for id, col in enumerate(cursor.description):
        d[col[0]] = row[id]
    return d

def dict_factory_multi(cursor, rows):
    d =  {}
    for part, row in enumerate(rows):
            d['part'+str(part)] = dict_factory_single(cursor, row)
    return d


def creat_tables():

    c = conn.cursor()

    # Create table project_ata
    c.execute('''CREATE TABLE project_data
                 (project TEXT, plant TEXT, project_name TEXT)''')


    # Create table part_data
    c.execute('''CREATE TABLE part_data
                 (project TEXT, nr_id TEXT, part TEXT, part_description TEXT,
                 mtl_group TEXT, raw_mtl TEXT, currency TEXT, risk_level TEXT,
                 buyer TEXT)''')

    # Create table project_timing
    c.execute('''CREATE TABLE project_timing
                 (project TEXT, part TEXT, ppap_date TEXT, tooling_weeks TEXT,
                 nomi_date TEXT, rfq_weeks TEXT, drawing_date TEXT)''')


    # Create table sourcing_concept
    c.execute('''CREATE TABLE sourcing_concept
                 (project TEXT, part TEXT, vendor TEXT, vendor_nominated TEXT,
                 vendor_active TEXT)''')


    # Create table rfq_part
    c.execute('''CREATE TABLE rfq_part
                 (project TEXT, part TEXT, year INTEGER, volume INTEGER,
                 target_price100 REAL)''')


    # Create table rfq_invest
    c.execute('''CREATE TABLE rfq_invest
                 (project TEXT, part TEXT, tool INTEGER, tool_description TEXT,
                 cav_target INTEGER, cost_target INTEGER, loop_target TEXT,
                 copy_tool_name TEXT, copy_tool_cost INTEGER, further_invest_name TEXT, further_invest_cost INTEGER)''')


    # Create table nomi_part
    c.execute('''CREATE TABLE nomi_part
                 (project TEXT, part TEXT, vendor TEXT, year INTEGER, price100
                 REAL, lta REAL, qs INTEGER, quota REAL)''')


    # Create table nomi_invest
    c.execute('''CREATE TABLE nomi_invest
                 (project TEXT, part TEXT, vendor TEXT, tool INTEGER,
                 nomi_date TEXT, cavity INTEGER, tool_cost INTEGER,
                 copy_tool_cost INTEGER, further_invest_cost INTEGER, currency
                 TEXT, nomi_ppap_date TEXT, nomi_fot_date TEXT,
                 nomi_loops TEXT, nomi_letter_signed TEXT)''')


    # Create table vendors
    c.execute('''CREATE TABLE vendors
                 (vendor TEXT, vendor_name TEXT, address TEXT, city TEXT,
                 province TEXT, country TEXT, delivery_reg_date TEXT,
                 tool_contract_date TEXT, framework_date TEXT, shifts_per_day
                 INTEGER, shift_duration INTEGER, days_per_week INTEGER,
                 weeks_per_year INTEGER, flex_pre INTEGER, flex_duration
                 INTEGER, flex_froz INTEGER)''')


    # Create table contacts
    c.execute('''CREATE TABLE contacts
                 (vendor TEXT, function TEXT, name TEXT, email TEXT,
                 phone TEXT)''')


    # Create table buyers
    c.execute('''CREATE TABLE buyers
                 (buyer TEXT, name TEXT, email TEXT,
                 phone TEXT)''')



    conn.commit()
    conn.close()



def nl_search_part_batch(project, vendor):

    c = conn.cursor()
    t = (project, vendor)

    c.execute('''SELECT * FROM rfq_part AS RP LEFT JOIN nomi_part AS NP ON
    RP.project=NP.project AND RP.part=NP.part AND RP.year=NP.year LEFT JOIN
    part_data AS PD ON RP.part=PD.part LEFT JOIN project_data AS PJD ON
    RP.project=PJD.project WHERE RP.project=? AND NP.vendor=?''', t) 

    print(c.fetchall())


def nl_search_part(project, vendor):

    # conn.row_factory = sqlite3.Row

    c = conn.cursor()
    t = (project, vendor)

    c.execute('''SELECT DISTINCT NP.project, PJD.project_name, NP.part, NP.vendor, PD.nr_id,
    PD.part_description, PD.mtl_group, PD.raw_mtl, PD.currency, PD.buyer FROM
    nomi_part AS NP LEFT JOIN part_data AS PD ON NP.part=PD.part LEFT JOIN
    project_data AS PJD ON NP.project=PJD.project WHERE NP.project=? AND NP.vendor=?''', t) 

    rows = c.fetchall()
    
    dict = dict_factory_multi(c, rows)
    print(dict)


    # titles = c.description
    # print(titles)

    return c.fetchall()



def nl_search_part_year(project, vendor):
    c = conn.cursor()
    t = (project, vendor)

    c.execute('''SELECT DISTINCT RP.part, RP.year, RP.volume, NP.vendor, NP.price100,
    NP.qs FROM rfq_part AS RP LEFT JOIN nomi_part AS NP ON RP.project=NP.project AND
    RP.part=NP.part AND RP.year=NP.year WHERE RP.project=? AND NP.vendor=?''', t) 

    print(c.fetchall())


# nl_search_part_year("1111P.000099", "48200025")


def nl_search_invest(project, vendor):
    c = conn.cursor()
    t = (project, vendor)

    c.execute('''SELECT * FROM nomi_invest AS NI WHERE NI.project=? AND
    NI.vendor=?''', t)  

    print(c.description)

    print(c.fetchall())

# nl_search_invest("1111P.000099", "48200025")


def nl_clear_nr(tables):
    for table in tables:
        c = conn.cursor()

        string = "DELETE FROM " + table
        print(string)

        c.execute(string)
        print(table + ' delected.')

    conn.commit()

# nl_clear_nr(['vendors', 'contacts', 'buyers'])

# nl_clear_nr(['project_data', 'part_data', 'project_timing', 'sourcing_concept',
    # 'rfq_part', 'rfq_invest', 'nomi_part', 'nomi_invest'])

if __name__ == "__main__":
    nl_search_part("1111E.001169", "48201484")



# conn.close()
