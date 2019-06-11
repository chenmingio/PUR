import sqlite3
conn = sqlite3.connect('nr.db')

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
             nomination_date TEXT, rfq_weeks TEXT, drawing_date TEXT)''')


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
             nomination_date TEXT, cavity INTEGER, tool_cost INTEGER,
             copy_tool_cost INTEGER, further_invest_cost INTEGER, currency
             TEXT, nomination_ppap_date TEXT, nomination_fot_date TEXT,
             nomination_loops TEXT, nomination_letter_signed TEXT)''')
