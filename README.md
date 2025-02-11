# 🚀 CryptoLiveTracker

CryptoLiveTracker is a Python-based project that fetches live cryptocurrency data using the **CoinMarketCap API** and stores it in a **Google Sheet**. It also generates a **PDF summary report** and updates a **Google Doc** with the latest market trends.
- Google Sheet - https://docs.google.com/spreadsheets/d/1VBzod4IfyC8c2wa_FOJF9MiNtvql6TL4NkGLRk0nFwM/edit?gid=0#gid=0
- Google Doc - https://docs.google.com/document/d/1S9tSZOj6zYyBfPSWQ3Pou1G42tVwprhxwMNqPdZin4o/edit?tab=t.0

## 📌 Features

- Fetches **real-time** cryptocurrency data (Top 50 coins).
- Stores data in an **Excel file** (`crypto_data.xlsx`).
- Uploads the data to a **Google Sheet** for easy access.
- Generates a **PDF summary report** of the market trends.
- Updates a **Google Doc** with the latest report.

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dhruvkhanna930/CryptoLiveTracker.git
cd CryptoLiveTracker
```

### 2️⃣ Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys

This project requires the **CoinMarketCap API Key** and **Google Service Account Credentials**.

#### 🔑 Get CoinMarketCap API Key:
1. Sign up at [CoinMarketCap Developer Portal](https://coinmarketcap.com/api/).
2. Get your **API Key** from the dashboard.

#### 📝 Create `.env` File:
Inside the project folder, create a `.env` file and add:

```env
COINMARKETCAP_API_KEY=your_api_key_here
```

---

### 4️⃣ Google API Setup (Google Sheets & Google Docs)
#### 🌍 Create Google Cloud Credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **New Project**.
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API
   - Google Docs API
4. Create a **Service Account**.
5. Download the `credentials.json` file and place it in the project directory.
6. Share the Google Sheet & Google Doc **edit access** with the service account email (`xyz@xyz.iam.gserviceaccount.com`).

---

## 🚀 Running the Script

Run the main script to fetch live data and generate reports:

```bash
python crypto_live_tracker.py
```

---

## 📜 Output

- `crypto_data.xlsx` → **Saved locally**
- **Google Sheet** → Uploaded data ✅
- `crypto_report.pdf` → **Saved locally**
- **Google Doc** → Updated with market summary ✅

---

## 🔧 Troubleshooting

- **Error: Push Declined Due to Repository Rule Violations**  
  *Solution:* If `credentials.json` was mistakenly committed, remove it using:

  ```bash
  git rm --cached credentials.json
  echo "credentials.json" >> .gitignore
  git commit -m "Removed credentials.json from repo"
  git push origin main
  ```

- **Google Authentication Issues?**  
  Make sure the service account email has **edit permissions** for Google Sheets & Docs.

---

## 🤝 Contribution

Feel free to fork the repository and contribute! 🚀

---

## 📜 License

MIT License © 2025 [Dhruv Khanna](https://github.com/dhruvkhanna930)
