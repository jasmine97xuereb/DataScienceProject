# Task 1: Analysing the Computer Science Papers Dataset 

The dblp file is scraped using the python script file extract_data.py.
This can be run by executing the command 'python extract_data.py' in the terminal.
Three new files, 'Author.csv', 'Article.csv', and 'Publish.csv' will be created. 
Duplicates must be removed by running the following commands:
	awk '!seen[$0]++' Author.csv >> Author.csv
	awk '!seen[$0]++' Article.csv >> Article.csv
	awk '!seen[$0]++' Publish.csv >> Publish.csv
After running a new neo4j docker container, import data into the neo4j graph database by running the following commands:
	docker exec -i -t some-neo4j /bin/bash
	neo4j-admin import --database=graph_db.db --input-encoding='iso-8859-1' --ignore-duplicate-nodes=true --nodes:Author /data/Author.csv --nodes:Article /data/Article.csv --relationships:PUBLISH /data/Publish.csv
Stop the running neo4j container and start a new one, setting the new graph database as the active database as following, replacing the path accordingly:
	docker run -v /c/Users/jasmi/Desktop/year4/DataScience/Assignment/task1/neo4j/logs:/logs --env=NEO4J_dbms_active__database=graph_db.db -v /c/Users/jasmi/Desktop/year4/DataScience/Assignment/Question1/neo4j/data:/data --name some-neo4j --env NEO4J_AUTH=none -p 7474:7474 -p 7687:7687 -d neo4j
Link the running container to analyse data on Jupyter lab. 	

# Task 2: Extracting and Visualising Data from EU Stats

Run Data_Extraction_And_Visualization.ipynb in Jupyter Lab to analyse the data.

# Task 3: Dataset Analysis

Scrape the html files by running the python script extract_data.py by the command 'python extract_data.py'.
A new file 'full_property_data.csv' will be created.
To extract the time and date from each log file run the following commands:
	for i in *.log; do head -2 "$i" >> log_dates.txt; done
	sed '/--/!d' log_dates.txt
A new file log_dates.txt will be created.
Run DatasetAnalysis.ipynb in Jupyter Lab to analyse the data.

