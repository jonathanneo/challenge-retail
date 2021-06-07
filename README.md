# The challenge

You have a file `Retail.csv` describing sales data for a hypothetical Camping Supplies store.
Using your tool of choice, answer the following questions:

1. Construct a report breaking down sales by country, sales channel, product and year. The report should be easy to navigate.

2. Provide a list of recommendations for improving the store's profit.

3. Predict the next year of sales for each country. Your predictions will be analysed by a statistically sophisticated manager.

4. What additional data would you want to collect? What analyses would it empower you to run?

# My solution

I have created a flask app to render different pages to answer the above questions.

# Running locally

1. Freeze pip / conda requirements

   ```
   python -m pip list --format=freeze > requirements.txt
   ```

2. Create the environment using

   ```
   conda create -n <env> --file requirements.txt
   ```

3. Run the app using:

   ```
   python app.py
   ```

   OR

   ```
   flask run
   ```

# Deploying to Heroku

1. Freeze pip / conda requirements

   ```
   python -m pip list --format=freeze > requirements.txt
   ```

2. Create/Update `Procfile` to use gunicorn to run the web server and set app.py as the application to run:

   ```
   web: gunicorn app:app
   ```

3. Create/Update `runtime.txt` to contain:

   ```
   python-3.7.10
   ```
