# Migroto
Migroto is a quick and dirty Python script that retrieves the mortgage rate from the [Migros bank website](https://www.migrosbank.ch/) and store it in a Google spreadsheet. It can easily be setup as a Google Cloud Function that can be run daily.

## Setup
This documents how to set up the script as a Google Cloud Function.

### Create and set up a Google Cloud project
Create a new Google Cloud project. In `APIs & Services > Library` enable the `Google Sheets` and `Google Drive` APIs.

In `APIs & Service > Credentials`, create a new `Service account`. Choose a service account name (`migroto` suggested) and id (`migroto` suggested). Grant the account the role `Basic > Editor`. Edit the newly created service account and create a new key for it in the JSON format. Download the key file and rename it `credentials.json`. Retain the e-mail of the service account (it should be `migroto@migroto.iam.gserviceaccount.com` with the suggested names).

### Create the Google spreadsheet
Create a new spreadsheet in your Google Drive. In the sharing settings, invite the service account created in the previous step as an editor of the file. In the URL of the spreadsheet, identify its id (it is a long alphanumeric string that can easily be spotted).

### Deploy Cloud Function
Back in the Google Cloud Platform console, go to `Cloud Functions` to create a new function. Choose a name (`migroto` suggested) and the region that will run the function. In the section `Trigger`, choose `Cloud Pub/Sub` and choose a name for the topic (`migroto` suggested).

Edit the newly created function and copy and paste the content of the files `main.py` and `requirements.txt`. Adjust the file `main.py` to update the id of the spreadsheet. Add the file `credentials.json` retrieved in the previous step along the other files. Choose the runtime `Python 3.9` and set the entry point to `update`.

You can then test the function using the dedicated button in the user interface. If it does not work, use the log to identify the issue.

### Setup scheduler
In Google Cloud Platform console, go to `Cloud Scheduler` to create a new job. Choose a name (`migroto` suggested) and select the same region as for the function. In `Frequency`, choose `0 10 * * *` to run the function every day at 10.

Configure the scheduler with the target type `Pub/Sub` and choose the same topics as for the function. In the message body, enter "NA".

## Development
First, install dependencies:
```
pip3 install -r requirements.txt
```

Then, edit the file `main.py` to update the id if the spreadsheet. Finally, execute the script with:
```
python3 main.py
```
