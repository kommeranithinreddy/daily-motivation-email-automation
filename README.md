\# Daily Motivation Email Automation



A Python automation project that sends a daily motivational email with a thoughtfully designed HTML newsletter.



The goal is to share a little positivity, encouragement, and motivation with recipients every day.



\## Features



\* \*\*Daily Motivational Quotes:\*\* Selects a quote based on the current date.

\* \*\*240 Motivational Entries:\*\* Includes eight categories covering learning, health, studying, goals, happiness, confidence, habits, and relationships.

\* \*\*Personalized Email Design:\*\* Sends a visually appealing newsletter with a cream-and-gold theme.

\* \*\*HTML and Plain-Text Support:\*\* Provides HTML formatting with a plain-text alternative.

\* \*\*Multiple Recipients:\*\* Manages recipient email addresses through a JSON file.

\* \*\*Gmail Integration:\*\* Sends emails through Gmail SMTP.

\* \*\*Environment Variables:\*\* Keeps email credentials in a local `.env` file.

\* \*\*Daily Automation Ready:\*\* Can be scheduled using Windows Task Scheduler.



\## Technologies Used



\* Python

\* JSON

\* SMTP

\* HTML

\* `python-dotenv`

\* Gmail SMTP



\## Project Structure



```text

daily-motivation-email-automation/

├── src/

│   ├── main.py

│   ├── email\_sender.py

│   └── content\_manager.py

├── data/

│   ├── quotes.json

│   └── recipients.json

├── .env.example

├── .gitignore

├── requirements.txt

├── README.md

└── test\_content.py

```



\## Setup and Installation



\### 1. Clone the repository



```bash

git clone <your-repository-url>

cd daily-motivation-email-automation

```



Replace `<your-repository-url>` with your GitHub repository URL after publishing the project.



\### 2. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 3. Configure email credentials



Create a local `.env` file in the project root using `.env.example` as a reference.



Add your Gmail address and Gmail App Password:



```text

EMAIL\_ADDRESS=your\_email@gmail.com

EMAIL\_APP\_PASSWORD=your\_gmail\_app\_password

```



Use a Gmail App Password rather than your regular Google account password.



\*\*Security:\*\* Never commit `.env` or share your App Password publicly.



\### 4. Configure recipients



Edit `data/recipients.json` and add the email addresses of your intended recipients.



Example:



```json

\[

&#x20;   "recipient1@example.com",

&#x20;   "recipient2@example.com"

]

```



Replace the example addresses with actual recipient addresses.



\### 5. Run the application



From the project root, execute:



```bash

python -m src.main

```



The application selects the daily quote, creates the newsletter, and attempts to send the email to each configured recipient.



\### 6. Run the content test



To verify the motivational quote data and content manager, run:



```bash

python test\_content.py

```



\## How It Works



1\. The application selects a motivational entry based on the current date.

2\. It generates an HTML newsletter containing the quote, a short message, and the date.

3\. Recipient addresses are loaded from `data/recipients.json`.

4\. Emails are sent through Gmail SMTP.

5\. The application reports the delivery attempt results in the terminal.



The same quote is selected when the application runs multiple times on the same day. With 240 entries, the selection follows a daily cycle through the available entries.



\## Future Improvements



\* Automate daily execution with Windows Task Scheduler.

\* Improve delivery-status tracking if needed.

\* Expand the motivational content collection over time.

