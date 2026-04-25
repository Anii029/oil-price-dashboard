import pandas as pd
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv("oil.csv")

# show first 5 rows
print(df.head())
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["Price"], label="Oil Price")

plt.title("Oil Price Trend")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()

plt.show()
plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["Price"], label="Oil Price")

plt.axvline(pd.to_datetime("2022-02-24"),
            color="red", linestyle="--",
            label="War Start")

plt.title("Oil Prices vs War")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()

plt.show()
before = df[df["Date"] < "2022-02-24"]
after = df[df["Date"] >= "2022-02-24"]
print("Average price BEFORE war:", before["Price"].mean())
print("Average price AFTER war:", after["Price"].mean())
impact = after["Price"].mean() - before["Price"].mean()
print("Impact (increase in price):", impact)
before_avg = before["Price"].mean()
after_avg = after["Price"].mean()
plt.axhline(before_avg, color="green", linestyle="--", label="Before Avg")
plt.axhline(after_avg, color="orange", linestyle="--", label="After Avg")
# Labels
plt.title("Oil Prices Before vs After War")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()

plt.show()