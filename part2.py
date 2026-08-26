import sqlite3
import pandas as pd

connection = sqlite3.connect("immune.db")
cursor = connection.cursor()

print("Part 2")
cursor.execute("""WITH totalCount AS (SELECT sample, SUM(count) AS total_count FROM cell_counts GROUP BY sample)
                  SELECT CC.sample,
                         TC.total_count,
                         CC.cell_type AS population,
                         CC.count,
                         ROUND((CC.count * 100.0 / TC.total_count),2) AS percentage
                  FROM cell_counts AS CC
                  JOIN totalCount AS TC ON TC.sample = CC.sample
                  ORDER BY CC.sample ASC""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['sample', 'total_count', 'population', 'count', 'percentage'])
print(results_df)
print("\n")
results_df.to_csv(f'outputs/part2/part2.csv', index = False)

connection.close()