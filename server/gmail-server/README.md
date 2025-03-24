# Gmail API Integration Setup Guide

This guide will walk you through setting up a Google Cloud project, enabling the Gmail API, creating OAuth 2.0 credentials, and preparing your environment to use the Gmail API with this project.

## Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.x:** This project is built using Python.
*   **Pip:** Python's package installer.
*   **A Google Account:** You'll need a Google account to access the Google Cloud Console.
* **Installed dependencies:** Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
    This will install the following packages:
    * `mcp[cli]` and `mcp`: Likely a custom package used in the project.
    * `httpx`: A modern HTTP client for Python.
    * `dotenv`: For managing environment variables.
    * `google-api-python-client`: The official Google API client library for Python.
    * `google-auth-oauthlib`: For handling OAuth 2.0 authentication with Google.

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1.  Go to the Google Cloud Console.
2.  Click on the project dropdown menu at the top of the page.
3.  Click "New Project."
4.  Enter a project name (e.g., "My Gmail Integration") and click "Create."

### 2. Enable the Gmail API

1.  In the Google Cloud Console, navigate to "APIs & Services" > "Library."
2.  Search for "Gmail API."
3.  Click on "Gmail API" in the search results.
4.  Click the "Enable" button.

### 3. Configure the OAuth Consent Screen

1.  In the Google Cloud Console, go to "APIs & Services" > "OAuth consent screen."
2.  Select the "External" user type if you intend to use this outside of a Google Workspace organization. Otherwise, choose "Internal".
3.  Click "Create."
4.  Fill in the required information:
    *   **App name:** A name for your application (e.g., "My Gmail App").
    *   **User support email:** Your email address.
    *   **App logo:** (Optional)
    *   **App domain:** (Optional)
    *   **Authorized domains:** (Optional)
    *   **Developer contact information:** Your email address.
5.  Click "Save and Continue".
6.  On the Scopes page, click "Add or Remove Scopes".
7.  Search for `https://www.googleapis.com/auth/gmail.readonly` (or other scopes you need) and select it, Select all the scope to make agent work with gmail completely.
8.  Click "Update" and then "Save and Continue".
9.  On the Test users page, add your email address as a test user.
10. Click "Save and Continue" and then "Back to Dashboard".

### 4. Create OAuth 2.0 Credentials

1.  In the Google Cloud Console, go to "APIs & Services" > "Credentials."
2.  Click "+ Create Credentials" and select "OAuth client ID."
3.  Choose "Web application" as the application type.
4.  Enter a name for your client (e.g., "Gmail Client").
5.  Under "Authorized redirect URIs," add `http://localhost:50505/`. This is the URL your application will use to receive the authorization code after the user grants permission.
6.  Click "Create."

### 5. Download and Rename Credentials

1.  After creating the OAuth client ID, you'll see a popup with your client ID and client secret.
2.  Click the download icon (a downward arrow) next to your newly created client. This will download a JSON file containing your credentials.
3.  Rename the downloaded JSON file to `credentials.json`.

### 6. Place Credentials in the Project Directory

1.  Move the `credentials.json` file to the same directory where your main Python script (that interacts with the Gmail API) is located.

### 7. Run Your Application

1.  Ensure you have installed all the dependencies listed in `requirements.txt`
2.  Run your Python script. The first time you run it, it will likely open a browser window to prompt you to authorize the application to access your Gmail account.
3.  After authorization, the application will receive an access token and can start interacting with the Gmail API.

## Important Notes

*   **Security:** Keep your `credentials.json` file secure. Do not commit it to version control (e.g., Git). Consider using environment variables to manage sensitive information.
*   **Scopes:** Be mindful of the scopes you request. Only request the minimum necessary permissions.
*   **Testing:** If you are using the "External" user type, you will need to add your email as a test user.
* **Port:** Ensure that the port `50505` is not already in use on your machine.
* **Error Handling:** Implement proper error handling in your code to deal with potential issues like network problems, invalid credentials, or API errors.
