# FabLIMS to NOMAD Synchronization

This folder contains the automated synchronization script (`sync_fablims.py`) that extracts instrument data from the FabLIMS API, formats it into NOMAD `.archive.json` files, and automatically uploads it to the iEntrance NOMAD Oasis via the API.

## Prerequisites
* Python 3.10+
* Access to the iEntrance NOMAD Oasis.
* A valid FabLIMS API Key.
* A NOMAD App Token.

---

## Step 1: Environment Setup

Before running the script, create an isolated Python environment and install the required dependencies.

1. Open your terminal and navigate to the `scripts/` folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```
3. Activate the virtual environment:
```bash
source .venv/bin/activate
```
4. Install the required packages:
```bash
pip install requests
```

## Step 2: Configuration & API Keys

For security reasons, API keys are never hardcoded into the script. We use a hidden `.env` file to manage secrets securely.

1. Create a copy of the provided template file:
```bash
cp .env.example .env
```
2. Open the new `.env` file in your text editor.

3. Fill in your secure keys:
    - `FABLIMS_API_KEY`: Request this from your FabLIMS administrator.
    - `NOMAD_PERSONAL_ACCESS_TOKEN`: Generate this by logging into your iEntrance NOMAD Oasis. In the top menu, navigate to **ANALYZE > APIs** and generate an **App token**. Copy the resulting token string.

## Step 3: Script Configuration (Target URL)

By default, the script will automatically upload the data to the live iEntrance Oasis (`https://oasis.ientrance.eu/nomad-oasis/api/v1`).
If you want to test the script against a local development environment instead, you can override this URL:

1. Open your `.env` file.
2. Add the `NOMAD_BASE_URL` variable and point it to your local environment.
3. Save the file


## Step 4: Running the Script

Once your environment is active, your `.env` file is configured, and the URL is set, you are ready to run the extraction and upload process.

1. Load your environment variables and execute the script:

```Bash
set -a; source .env; set +a
python sync_fablims.py
```

## Expected Output

If successful, the script will output the following in your terminal:

1. The total number of instruments successfully fetched and converted into `.archive.json` files (saved in the `nomad_upload/` folder).

2. A confirmation that the files were zipped.

3. A success message from the NOMAD API alongside your new **Upload ID**.

You can view the uploaded instruments immediately by opening your NOMAD Oasis GUI and navigating to the **PUBLISH > Uploads** page!