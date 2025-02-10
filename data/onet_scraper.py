import pandas as pd
from playwright.sync_api import sync_playwright

# Load CSV file
csv_path = "careers_in_sa.csv"
df = pd.read_csv(csv_path)

# Ensure the CSV has the expected column
if "name" not in df.columns:
    raise ValueError("CSV file must contain a column named 'name'.")

# Add a new column for the interest codes
df["interest_code"] = ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set to True for faster execution
    page = browser.new_page()
    base_url = "https://www.onetonline.org/"

    for index, row in df.iterrows():
        career_name = row["name"]

        page.goto(base_url)
        search_input = page.locator("#headersearchlg")
        search_input.fill(career_name)
        search_input.press("Enter")
        page.wait_for_load_state("networkidle")

        # Find the first career link
        first_cell_attr = page.locator(".sorter-text a").nth(1)

        if not first_cell_attr.count():
            print(f"No results found for {career_name}")
            continue

        new_link = first_cell_attr.get_attribute("href")
        if new_link:
            page.goto(new_link)

            # Extract the interest code
            if page.locator("#Interests").count>0 :
                interest_code_parent = page.locator("#Interests div").nth(1).locator("div").first.locator("b").first
                interest_code = interest_code_parent.inner_text().strip()
            else: 
                interest_code = "N/A"

            # Store the result in the DataFrame
            df.at[index, "interest_code"] = interest_code
            print(f"{career_name}: {interest_code}")

    browser.close()

# Save the updated CSV
output_path = "updated_careers.csv"
df.to_csv(output_path, index=False)
print(f"Updated CSV saved to {output_path}")
