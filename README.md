# Teiko Technical Assessment

## INSTRUCTIONS
*Make sure cell-count.csv is in the root directory.*
To setup the loading of the data, enter "make setup" inside the terminal. This will load the cell-count.csv and create the relational database.
To make the pipeline (parts 2-4), enter "make pipeline" inside the terminal. This will run all the parts and create all the tables and plots.
To make the dashboard, enter "make dashboard" inside the terminal. This will create the dashboard and provide the url to host.

## RELATIONAL DATABASE
I decided to split up the data into a number of tables in order to reduce redundancy while maintaining the appropriate relationships. This is how I broke it up:
PK = Primary Key, FK = Foreign Key
- projects (projects PK)
- subjects (subject PK, condition, age, sex)
- samples (sample PK, project FK, subject FK, sample_type, treatment, response, time_from_treatment_start)
- cell_counts (sample FK, cell_type, count)

I broke subjects into its own table so that if a subject's info changes or is involved in multiple samples, their information can stay consistent across samples.

I also broke samples into its own table with just information about that sample. I did this so that we can analyze just the results of the sample without having to also keep track of subject information and cell counts at the same time.
If we need that additional information, we can just do a simple join for either the subject information or the cell count information.

Splitting projects and cell counts likely deserve the most explanation. I broke off projects into its own table for two main reasons. One, so that we can track the number of projects we've done and easily find one. This scales well if we reach hundreds of projects and ensures that every project remains even if all the samples' rows involving it get deleted. 
Secondly, splitting projects allows us to keep counts of project samples even when no samples have been made yet. We saw this come into action in Part 4, where project2 had 0 samples in our subset. Without a separate table, this would have been lost and left up to assumption. 

Breaking cell-counts on its own was done to scale easily and allow for updates to the samples going forward. If we add a new cell type to study, we don't have to update every single sample previously done with a new column with NULL, we just add a new row to the cell count table and keep going.  

## CODE
My code structure is divided by parts, which is done both to keep things organized but also to make checking work easily. For example, my dashboard shows p-values for differences in frequency but does not show the calculations. That is reserved for the part3 file, so someone who is interested in seeing it can quickly and easily verify the calculations.
For calculations, Most statistical calculations are done manually to ensure accuracy and readability. Most counts and filtering are done using SQL, and t-tests are calculated manually up until checking the p-value for the t-stat. I did this so that anyone reading the files can understand how those values were found, and to minimize the number of packages the user would need to install.   

## LINKS
https://andrewsousateikotechical.streamlit.app/
