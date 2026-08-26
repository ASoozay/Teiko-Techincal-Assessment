import sqlite3
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
from scipy.stats import t
import math

connection = sqlite3.connect("immune.db")
cursor = connection.cursor()

cursor.execute("""WITH totalCount AS (SELECT sample, SUM(count) AS total_count FROM cell_counts GROUP BY sample),
                        samplePercentages AS (SELECT CC.sample,
                                                     TC.total_count,
                                                     CC.cell_type AS population,
                                                     CC.count,
                                                     CC.count * 100.0 / TC.total_count AS percentage
                                                FROM cell_counts AS CC
                                                JOIN totalCount AS TC ON TC.sample = CC.sample
                                                JOIN samples AS S ON S.sample = CC.sample
                                                JOIN subjects AS S2 ON S2.subject = S.subject
                                                WHERE S2.condition = 'melanoma'
                                                AND S.sample_type = 'PBMC'
                                                AND S.treatment = 'miraclib'
                                                ORDER BY CC.sample ASC)
                   SELECT S.response,
                          SP.population AS population,
                          ROUND(AVG(SP.percentage),2) AS avg_percentage  
                   FROM samplePercentages AS SP
                   JOIN samples AS S on S.sample = SP.sample
                   GROUP BY S.response, SP.population
                   ORDER BY SP.population ASC""")

results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['response', 'population', 'avg_percentage'])
results_df.to_csv(f'outputs/part3/frequency.csv', index = False)
print("\n")

cursor.execute("""WITH totalCount AS (SELECT sample, SUM(count) AS total_count FROM cell_counts GROUP BY sample),
                        samplePercentages AS (SELECT CC.sample,
                                                     S.response,   
                                                     CC.cell_type AS population,
                                                     CC.count * 100.0 / TC.total_count AS percentage
                                                FROM cell_counts AS CC
                                                JOIN totalCount AS TC ON TC.sample = CC.sample
                                                JOIN samples AS S ON S.sample = CC.sample
                                                JOIN subjects AS S2 ON S2.subject = S.subject
                                                WHERE S2.condition = 'melanoma'
                                                AND S.sample_type = 'PBMC'
                                                AND S.treatment = 'miraclib'
                                                ORDER BY CC.sample ASC)
                   SELECT *
                   FROM samplePercentages
                   """)
results = cursor.fetchall()
results_df = pd.DataFrame(results, columns = ['sample', 'response', 'population', 'percentage'])

sea.boxplot(
    data=results_df,
        x='population',
        y='percentage',
        hue= 'response'
    )

plt.xlabel('Response')
plt.ylabel('Relative Frequency (%)')
plt.title('Relative Frequency by Treatment Response')

plt.savefig(f'outputs/part3/boxplot.png', dpi=300, bbox_inches='tight')

sea.histplot(
    data=results_df,
    x='percentage',
    hue='response',
    kde=True
)

summary = results_df.groupby(['population', 'response'])['percentage'].agg(
    mean='mean',
    sd='std',
    n='count'
).reset_index()
summary.to_csv(f'outputs/part3/summary.csv', index = False)

populations = results_df['population'].unique()
for population in populations:
    results_pop = results_df[results_df['population'] == population]

    sea.histplot(
        data=results_pop,
        x='percentage',
        hue='response',
        kde=True
    )

    plt.xlabel('Relative Frequency (%)')
    plt.ylabel('Count')
    plt.title(f'{population} Relative Frequency')

    filename = population.replace(' ', '_')

    plt.savefig(f'outputs/part3/{filename}_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()

print("Looking at the histograms of the different cell populations, the distributions of all appear to be roughly normal \n"
      "Additionally, our response groups and independent and have similar variances. \n"
      "So, we can do a t-test to see if there's a significant difference in average percentages")
print("\n")

p_values = []
index = 0
for population in populations:

    summary_pop = summary[summary['population'] == population]

    pop_no = summary_pop[summary_pop['response'] == "no"]
    pop_yes = summary_pop[summary_pop['response'] == "yes"]

    x1 = pop_yes['mean'].iloc[0]
    x2 = pop_no['mean'].iloc[0]
    s1 = pop_yes['sd'].iloc[0]
    s2 = pop_no['sd'].iloc[0]
    n1 = pop_yes['n'].iloc[0]
    n2 = pop_no['n'].iloc[0]

    sp = math.sqrt(((n1 - 1)*s1**2 + (n2-1)*s2**2)/(n1 + n2 - 1))

    t_stat = (x1 - x2) / (sp*math.sqrt(1/n1 + 1/n2))

    df = n1 + n2 - 2

    p_value = 2 * (1 - t.cdf(abs(t_stat), df))
    p_values.append({'cell_type': population, 'p-value': p_value})
    index = index+1

    print(
        population,
        "t =", round(t_stat, 3),
        "df =", df,
        "p =", round(p_value, 4)
    )
p_values = pd.DataFrame(p_values)
p_values.to_csv('outputs/part3/p_values.csv', index = False)
print("\n")
print("Looking at the p-values for our tests, at alpha = 0.05 \n"
      "Between the yes responders and no responders, there is a statistically significant difference between the average relative percentages in cell count for cd4_t_cell. \n"
      )

connection.close()
