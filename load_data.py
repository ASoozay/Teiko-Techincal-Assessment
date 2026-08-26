import sqlite3
import pandas as pd

immune_data = pd.read_csv('cell-count.csv')

projects = immune_data[["project"]].drop_duplicates()
subjects = immune_data[["subject", "condition", "age", "sex"]].drop_duplicates()
samples = immune_data[["sample", "project", "subject", "sample_type", "treatment", "response", "time_from_treatment_start"]]
cell_counts = immune_data[["sample", "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]]
cell_counts = cell_counts.melt(id_vars=["sample"], var_name = "cell_type", value_name = "count")

connection = sqlite3.connect("immune.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS cell_counts")
cursor.execute("DROP TABLE IF EXISTS samples")
cursor.execute("DROP TABLE IF EXISTS projects")
cursor.execute("DROP TABLE IF EXISTS subjects")

cursor.execute("CREATE TABLE projects (project TEXT PRIMARY KEY)")
projects.to_sql("projects", connection, if_exists = "append", index = False)

cursor.execute("""CREATE TABLE subjects (subject TEXT PRIMARY KEY,
                                         condition TEXT NOT NULL,
                                         age INTEGER NOT NULL,
                                         sex TEXT NOT NULL)""")
subjects.to_sql("subjects", connection, if_exists = "append", index = False)

cursor.execute("""CREATE TABLE samples (sample TEXT PRIMARY KEY,
                                        project TEXT,
                                        subject TEXT,
                                        sample_type TEXT NOT NULL,
                                        treatment TEXT NOT NULL,
                                        response TEXT,
                                        time_from_treatment_start INTEGER NOT NULL,
                                        
                                        FOREIGN KEY (project) REFERENCES projects (project),
                                        FOREIGN KEY (subject) REFERENCES subjects (subject))""")
samples.to_sql("samples", connection, if_exists = "append", index = False)

cursor.execute("""CREATE TABLE cell_counts (sample TEXT,
                                            cell_type TEXT NOT NULL,
                                            count INTEGER NOT NULL,
                                            
                                            FOREIGN KEY (sample) REFERENCES samples (sample))""")
cell_counts.to_sql("cell_counts", connection, if_exists = "append", index = False)

