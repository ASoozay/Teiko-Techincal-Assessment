import sqlite3
import pandas as pd

connection = sqlite3.connect("immune.db")
cursor = connection.cursor()

cursor.execute("""SELECT samples.sample, samples.subject, subjects.condition, samples.treatment, samples.sample_type, samples.time_from_treatment_start 
                  FROM samples
                  JOIN subjects ON subjects.subject = samples.subject
                  WHERE samples.sample_type = 'PBMC'
                  AND subjects.condition = 'melanoma'
                  AND samples.time_from_treatment_start = 0
                  AND samples.treatment = 'miraclib'""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['sample', 'subject', 'condition', 'treatment', 'sample_type', 'time_from_treatment_start'])
print("Part 4 Question 1")
print(results_df)
results_df.to_csv(f'outputs/part4/1.csv', index = False)
print("\n")

print("Part 4 Question 2.1")
cursor.execute("""SELECT 
        projects.project,
        COUNT(samples.sample) AS sample_count
    FROM projects
    LEFT JOIN samples 
        ON samples.project = projects.project
        AND samples.sample_type = 'PBMC'
        AND samples.time_from_treatment_start = 0
        AND samples.treatment = 'miraclib'
    LEFT JOIN subjects 
        ON subjects.subject = samples.subject
        AND subjects.condition = 'melanoma'
    GROUP BY projects.project
    ORDER BY projects.project""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['project', 'count'])
print(results_df)
results_df.to_csv(f'outputs/part4/2_1.csv', index = False)
print("\n")

print("Part 4 Question 2.2")
cursor.execute("""SELECT 
        samples.response,
        COUNT(samples.sample) AS sample_count
    FROM projects
    LEFT JOIN samples 
        ON samples.project = projects.project
        AND samples.sample_type = 'PBMC'
        AND samples.time_from_treatment_start = 0
        AND samples.treatment = 'miraclib'
    LEFT JOIN subjects 
        ON subjects.subject = samples.subject
        AND subjects.condition = 'melanoma'
    GROUP BY samples.response
    ORDER BY projects.project ASC""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['response', 'count'])
print(results_df)
results_df.to_csv(f'outputs/part4/2_2.csv', index = False)
print("\n")

print("Part 4 Question 2.3")
cursor.execute("""SELECT subjects.sex,
                         COUNT(samples.sample) AS sample_count
                    FROM projects
                    LEFT JOIN samples 
                    ON samples.project = projects.project
                    AND samples.sample_type = 'PBMC'
                    AND samples.time_from_treatment_start = 0
                    AND samples.treatment = 'miraclib'
                LEFT JOIN subjects 
                    ON subjects.subject = samples.subject
                    AND subjects.condition = 'melanoma'
                GROUP BY subjects.sex
                ORDER BY projects.project ASC""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['sex', 'count'])
print(results_df)
results_df.to_csv(f'outputs/part4/2_3.csv', index = False)
print("\n")

print("Final Qustion")
cursor.execute("""SELECT ROUND(AVG(CC.count), 2)
                  FROM cell_counts AS CC
                  JOIN samples on samples.sample = CC.sample
                  JOIN subjects ON subjects.subject = samples.subject
                  WHERE subjects.sex = 'M'
                  AND subjects.condition = 'melanoma'
                  AND samples.response = "yes"
                  AND samples.time_from_treatment_start = 0
                  AND CC.cell_type = 'b_cell'""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['count'])
print(results_df)
results_df.to_csv(f'outputs/part4/3.csv', index = False)
print("\n")

connection.close()