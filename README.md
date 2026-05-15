# Creating a Chatbot to Interact with Your Database

NOTES:<br>
1 - After looking for a lot of publications, I could not find any trustfull that helped me to improve my process using genie API. So this application can help you to create similar project to interact with your database.<br>
2 - The credentials is personal so it is blank to keep the confidentiality.<br>


Since joining General Motors, I have focused on implementing solutions that accelerate daily operations, reduce manual effort, and improve process reliability. Several activities that previously required two to three days are now automated and refreshed daily, including sales, demand, and parts databases. The integration of tax-related information into the parts database enhanced and strengthened the pricing process.
This article presents the development of a chatbot designed to interact with business data through Databricks Genie. In future chapters, I will provide additional detail on database ingestion in Databricks and the development of gold-layer visualizations for business users.
1.	Project Objective<br>
The main objective was to implement a chatbot capable of helping users quickly retrieve information related to daily sales, monthly sales, warranty data, and other key business indicators. The goal was to make data access more intuitive, faster, and more scalable for end users.
2.	Data Foundation<br>
The first step was to ingest the required databases into Databricks. This phase was supported by the IT team, which helped transfer the necessary databases from Oracle into the Databricks environment.
Once the data was available in Databricks, the next step was to create gold-layer databases to provide Genie with curated and business-ready information. This stage required additional effort because SAP databases often use technical column names, making it necessary to identify and map each field correctly.
After this preparation, I created an SQL query scheduled to run daily so that the sales database would always be updated with the latest information.
3.	Creating the Genie Space<br>
After the data engineering activities were completed, the second phase was to create a Genie space.
3.1	Open Databricks and navigate to Genie Spaces.<br>
3.2	Create a new Genie space.<br>
3.3	Select the database that will be used as the source for Genie. In this case, I selected the sales database.<br>
3.4	Complete the creation process.<br>
At this stage, Genie is already available to interact with the sales database.<br>
An important consideration is that Genie may initially return inaccurate or incomplete interpretations. To improve accuracy, it is necessary to provide business context, definitions, and classification rules. For example, if the business uses codes to distinguish genuine parts, accessories, and other categories, this information should be added so Genie can interpret results correctly. The same principle applies to all important business fields across the database.<br>
 
4.	Sharing and Integration<br>
Once the Genie space is implemented, it can be shared with other users or connected to a website through the API. For this integration, I used Python.<br>
To connect the Genie space to the website, I used the Databricks library, the WorkspaceClient class, requests, and Streamlit. The final application was deployed using Databricks Apps.<br>
The main libraries and components were necessary to build a secure and scalable integration process. I also created an environment to store secret information securely and pass credentials safely to the application. Credentials such as the Databricks client ID and secret were removed from the published examples. This is an important best practice to avoid conflicts with personal or production credentials.
Because token-based connections were not permitted in my case, the connection was configured using credentials through an approved authentication method.<br>
5.	Web Integration and Deployment<br>
The solution was extended into a web application using:<br>
•	Python
•	Databricks SDK (WorkspaceClient)
•	Requests library (API calls)
•	Streamlit (frontend interface)
 
Secure environment variables were used to store credentials and connection details:
 
The application was deployed using Databricks Apps, making it accessible to end users.
API Integration with Genie
To interact with Genie via API, two key parameters are required:<br>
•	GENIE_URL (Databricks workspace URL)<br>
•	GENIE_SPACE_ID (Unique identifier of the chatbot space)<br>
 
Authentication is handled using a Service Principal (Entra ID) via the Databricks SDK:
 
6.	Query Execution Flow<br>
The chatbot interaction follows these steps:<br>
6.1	Start conversation<br>
6.2	Wait for processing completion<br>
6.3	Retrieve results<br>
6.4	Final function implementation<br>
 
7.	Data Processing and Presentation
Responses returned by Genie are in JSON format. These are processed and transformed into structured DataFrames<br>
- The application preserves query history and displays responses using Streamlit<br>
- Final output example can be viewed in the code.<br>

8.	Business Value
This solution demonstrates how a well-structured data foundation combined with Databricks Genie can improve access to business information. By connecting curated databases to a conversational interface, users can obtain relevant answers more quickly and with less dependence on manual analysis. 
The project also reinforces the importance of strong data engineering practices, secure integration standards, and business-context enrichment to ensure better accuracy and more reliable user experience.
9.	Conclusion
Creating a chatbot to interact with business databases is not only a technical implementation but also a strategic step toward improving operational efficiency and data accessibility. With the right data preparation, governance, and integration approach, conversational interfaces can become valuable tools for supporting business decisions and enhancing productivity across teams.

