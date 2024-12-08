import pandas as pd
import matplotlib.pyplot as plt

# Load data from Excel file
file_path = input("Enter the path to your Excel file (e.g., loan_data.xlsx): ")
try:
    df = pd.read_excel(file_path)
    print("Loan data loaded successfully!")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Display the first few rows of the dataset for confirmation
print("\nPreview of the Loan Data:")
print(df.head())

# Define covenant thresholds
max_dti = float(input("\nEnter maximum allowable Debt-to-Income Ratio (%): "))
max_ltv = float(input("Enter maximum allowable Loan-to-Value Ratio (%): "))

# Identify breaches
df["DTI Breach"] = df["Debt-to-Income Ratio (%)"] > max_dti
df["LTV Breach"] = df["Loan-to-Value Ratio (%)"] > max_ltv

# Generate risk mitigation recommendations
def recommend_action(row):
    actions = []
    if row["DTI Breach"]:
        actions.append("Reduce loan amount or increase borrower income.")
    if row["LTV Breach"]:
        actions.append("Increase down payment or reduce loan amount.")
    return "; ".join(actions)

df["Recommendations"] = df.apply(recommend_action, axis=1)

# Save the recommendations and breaches summary to an Excel file
output_file = "breach_recommendations.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")
print(f"Breach and recommendations summary saved to {output_file}")

# Plot color-coded risk distribution
if "Risk Rating" in df.columns:
    plt.figure(figsize=(8, 5))
    colors = {"Low": "lightgreen", "Medium": "gold", "High": "salmon"}
    df["Risk Rating"].value_counts().plot(
        kind="bar",
        color=[colors.get(rating, "blue") for rating in df["Risk Rating"].value_counts().index],
    )
    plt.title("Risk Rating Distribution")
    plt.xlabel("Risk Rating")
    plt.ylabel("Number of Loans")
    plt.tight_layout()
    risk_chart_file = "risk_distribution_colored.png"
    plt.savefig(risk_chart_file)
    plt.show()
    print(f"Risk distribution chart saved as {risk_chart_file}")
else:
    print("Column 'Risk Rating' not found in the dataset. Skipping risk distribution chart.")

# Display a preview of the final data with recommendations
print("\nFinal Data with Breach and Recommendations:")
print(df[["Loan ID", "Borrower Name", "DTI Breach", "LTV Breach", "Recommendations"]].head())
