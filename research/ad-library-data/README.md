# Ad Library Data

Place raw competitor ad data here. The Strategist will analyze this folder.

## How to Populate This Folder

### Method 1: Meta Ad Library (Free — Manual)
1. Go to https://www.facebook.com/ads/library
2. Search for your competitor's page name
3. Filter: Country = **India**, Status = **Active**
4. Take screenshots or copy ad text manually
5. Save files here as: `[competitor-name]-ads-[date].txt` or `.json`

### Method 2: Apify Free Tier (25,000 credits = ~25k ads)
1. Sign up at https://apify.com (free tier available)
2. Use **"Facebook Ads Library Scraper"** actor
3. Export as JSON or CSV
4. Save here as: `apify-[competitor]-[date].json`

## File Naming Convention
```
competitor-name-YYYY-MM-DD.json    ← Apify export
competitor-name-YYYY-MM-DD.txt     ← Manual notes
screenshots/                       ← Screenshots folder
```
