import pandas as pd

# Sample data for 50 beverages
data = {
    "Name": [
        "Coca-Cola 12oz Can", "Pepsi 12oz Can", "Red Bull 8.4oz Can", "Monster Energy 16oz Can",
        "Sprite 12oz Can", "Mountain Dew 12oz Can", "Diet Coke 12oz Can", "Dr Pepper 12oz Can",
        "Gatorade 20oz Bottle", "Powerade 20oz Bottle", "Coca-Cola 20oz Bottle", "Pepsi 20oz Bottle",
        "Red Bull 12oz Can", "Monster Energy 24oz Can", "Sprite 20oz Bottle", "Mountain Dew 20oz Bottle",
        "Diet Coke 20oz Bottle", "Dr Pepper 20oz Bottle", "Gatorade 32oz Bottle", "Powerade 32oz Bottle",
        "Coca-Cola 2L Bottle", "Pepsi 2L Bottle", "Sprite 2L Bottle", "Mountain Dew 2L Bottle",
        "Diet Coke 2L Bottle", "Dr Pepper 2L Bottle", "Gatorade 64oz Bottle", "Powerade 64oz Bottle",
        "Coca-Cola 16.9oz Bottle", "Pepsi 16.9oz Bottle", "Sprite 16.9oz Bottle", "Mountain Dew 16.9oz Bottle",
        "Diet Coke 16.9oz Bottle", "Dr Pepper 16.9oz Bottle", "Gatorade 12oz Bottle", "Powerade 12oz Bottle",
        "Red Bull 16oz Can", "Monster Energy 32oz Can", "Sprite 8oz Can", "Coca-Cola 8oz Can",
        "Pepsi 8oz Can", "Mountain Dew 8oz Can", "Diet Coke 8oz Can", "Dr Pepper 8oz Can",
        "Coca-Cola 12oz Glass Bottle", "Pepsi 12oz Glass Bottle", "Sprite 12oz Glass Bottle", 
        "Mountain Dew 12oz Glass Bottle", "Diet Coke 12oz Glass Bottle", "Dr Pepper 12oz Glass Bottle"
    ],
    "SKU": [
        "CC12CAN", "PE12CAN", "RB84CAN", "ME16CAN",
        "SP12CAN", "MD12CAN", "DC12CAN", "DP12CAN",
        "GA20BOT", "PO20BOT", "CC20BOT", "PE20BOT",
        "RB12CAN", "ME24CAN", "SP20BOT", "MD20BOT",
        "DC20BOT", "DP20BOT", "GA32BOT", "PO32BOT",
        "CC2LBOT", "PE2LBOT", "SP2LBOT", "MD2LBOT",
        "DC2LBOT", "DP2LBOT", "GA64BOT", "PO64BOT",
        "CC169BOT", "PE169BOT", "SP169BOT", "MD169BOT",
        "DC169BOT", "DP169BOT", "GA12BOT", "PO12BOT",
        "RB16CAN", "ME32CAN", "SP8CAN", "CC8CAN",
        "PE8CAN", "MD8CAN", "DC8CAN", "DP8CAN",
        "CC12GLS", "PE12GLS", "SP12GLS", 
        "MD12GLS", "DC12GLS", "DP12GLS"
    ],
    "Width": [
        2.6, 2.6, 2.1, 2.7,
        2.6, 2.6, 2.6, 2.6,
        3.0, 3.0, 3.0, 3.0,
        2.5, 2.8, 3.0, 3.0,
        3.0, 3.0, 3.5, 3.5,
        4.0, 4.0, 4.0, 4.0,
        4.0, 4.0, 4.5, 4.5,
        2.7, 2.7, 2.7, 2.7,
        2.7, 2.7, 3.2, 3.2,
        2.7, 3.1, 2.3, 2.3,
        2.3, 2.3, 2.3, 2.3,
        2.7, 2.7, 2.7, 
        2.7, 2.7, 2.7
    ],
    "Height": [
        4.83, 4.83, 5.2, 6.2,
        4.83, 4.83, 4.83, 4.83,
        8.5, 8.5, 8.5, 8.5,
        5.5, 7.5, 8.5, 8.5,
        8.5, 8.5, 10.0, 10.0,
        12.0, 12.0, 12.0, 12.0,
        12.0, 12.0, 11.5, 11.5,
        8.0, 8.0, 8.0, 8.0,
        8.0, 8.0, 6.5, 6.5,
        6.2, 10.0, 4.83, 4.83,
        4.83, 4.83, 4.83, 4.83,
        7.5, 7.5, 7.5, 
        7.5, 7.5, 7.5
    ],
    "Depth": [
        2.6, 2.6, 2.1, 2.7,
        2.6, 2.6, 2.6, 2.6,
        3.0, 3.0, 3.0, 3.0,
        2.5, 2.8, 3.0, 3.0,
        3.0, 3.0, 3.5, 3.5,
        4.0, 4.0, 4.0, 4.0,
        4.0, 4.0, 4.5, 4.5,
        2.7, 2.7, 2.7, 2.7,
        2.7, 2.7, 3.2, 3.2,
        2.7, 3.1, 2.3, 2.3,
        2.3, 2.3, 2.3, 2.3,
        2.7, 2.7, 2.7, 
        2.7, 2.7, 2.7
    ]
}

# Create DataFrame
df = pd.DataFrame(data)
# Save to CSV
print("HEllo")
# df.to_csv('products.csv', index=False)
