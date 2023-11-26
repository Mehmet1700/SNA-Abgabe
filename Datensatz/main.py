import pandas as pd

# Leeres Dataframe erstellen
df = pd.DataFrame()


# Funktion zum standardisieren des Datensatzes
def standardize_data(data):
    # timestamp wird auf 19 Zeichen gekürzt
    print("Timestamp wird gekürzt")
    data['timestamp'] = data['timestamp'].str[:19]
    # Timestamp wird in datetime-Objekt umgewandelt
    print("Timestamp wird in datetime-Objekt umgewandelt")
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    # Timestamp wird zu datetime64[s] umgewandelt
    print("Timestamp wird zu datetime64[s] umgewandelt")
    data['timestamp'] = data['timestamp'].astype('datetime64[s]')
    # Filtern der Einträge sodass nur Einträge vom 2023-07-20 00:00:00 bis 2023-07-20 15:59:59 angezeigt werden
    print("Filtern der Einträge sodass nur Einträge vom 2023-07-20 00:00:00 bis 2023-07-20 15:59:59 angezeigt werden")
    data = data[(data['timestamp'] >= '2023-07-20 00:00:00') & (data['timestamp'] <= '2023-07-20 15:59:59')]

    #Falls in dem Datensatz keine Einträge sind, dann überspringe die Schleife
    if data.empty:
        print("Keine Einträge vorhanden")
        return

    # Das Timestamp Format wird gekürzt, sodass nur noch die Stunden, Minuten und Sekunden angezeigt werden
    print("Das Timestamp Format wird gekürzt, sodass nur noch die Stunden, Minuten und Sekunden angezeigt werden")
    data['timestamp'] = data['timestamp'].dt.strftime('%H:%M:%S')
    # Umwandeln von Timestamp in einen integer
    print("Umwandeln von Timestamp in einen integer")
    data['timestamp'] = data['timestamp'].str.replace(':', '').astype(int)


    # pixel_color hexadezimal in Farbe umwandeln
    print("pixel_color hexadezimal in Farbe umwandeln")
    # Use .loc[] to set values in the original DataFrame
    data.loc[data['pixel_color'] == '#FF4500', 'pixel_color'] = 1
    data.loc[data['pixel_color'] == '#FFA800', 'pixel_color'] = 2
    data.loc[data['pixel_color'] == '#FFD635', 'pixel_color'] = 3
    data.loc[data['pixel_color'] == '#00A368', 'pixel_color'] = 4
    data.loc[data['pixel_color'] == '#3690EA', 'pixel_color'] = 5
    data.loc[data['pixel_color'] == '#B44AC0', 'pixel_color'] = 6
    data.loc[data['pixel_color'] == '#000000', 'pixel_color'] = 7
    data.loc[data['pixel_color'] == '#FFFFFF', 'pixel_color'] = 8


    # Umwandeln der Spalte pixel_color in int8
    print("Umwandeln der Spalte pixel_color in int8")
    # Use .loc[] to modify the original DataFrame
    data.loc[:, 'pixel_color'] = data['pixel_color'].astype('int8')


    # Lösche die Zeilen, in welcher die Spalte coodinate zwei Kommas oder mehr enthält
    print("Lösche die Zeilen, in welcher die Spalte coodinate zwei Kommas oder mehr enthält")
    data = data[data['coordinate'].str.count(',').lt(2)]
    # Die Spalte coordinate in zwei Spalten "x" und "y" aufteilen
    print("Die Spalte coordinate in zwei Spalten 'x' und 'y' aufteilen")
    data[['x', 'y']] = data['coordinate'].str.split(',', expand=True, n=1)

    # Die Spalten "x" und "y" in int32 umwandeln
    print("Die Spalten 'x' und 'y' in int32 umwandeln")
    data['x'] = data['x'].astype('int32')
    data['y'] = data['y'].astype('int32')
    # Die Spalte "coordinate" löschen
    print("Die Spalte 'coordinate' löschen")
    data = data.drop(columns=['coordinate'])

    # User werden pseudonymisiert durch eine Zahl
    print("User werden pseudonymisiert durch eine Zahl")
    data['user'] = data['user'].astype('category').cat.codes

    # Gebe alle Datentypen aus
    print("Datentypen des Datensatzes:")
    print(data.dtypes)
    return data


"""
Tabelle der Farben
rot = #ff4500 = 1
orange = #ffa800 = 2
gelb = #ffd635  = 3
grün = #00a368 = 4
blau = #3690ea = 5
lila = #b44ac0 = 6
schwarz = #000000 = 7
weiß = #ffffff = 8
"""

# Liste mit den csv.Dateien welche Daten vom 20.07.2023 enthalten
csvfiles = ["2023_place_canvas_history-000000000000.csv",
            "2023_place_canvas_history-000000000001.csv",
            "2023_place_canvas_history-000000000002.csv",
            "2023_place_canvas_history-000000000003.csv",
            "2023_place_canvas_history-000000000004.csv", ]

# Schleife für jede csv in der Liste
for file in csvfiles:
    # Lade die csv.Datei
    csv = pd.read_csv(file, delimiter=",")
    # Gib den Namen der csv.Datei aus
    print(file)
    # Standardisiere die csv.Datei
    standardcsv = standardize_data(csv)
    # Füge die csv.Datei in das Dataframe mit concat hinzu
    df = pd.concat([df, standardcsv], ignore_index=True)

# Informationen über df ausgeben
print(df.info())
print(df.head())
print(df.shape)

# Speichern des Dataframes in eine csv.Datei
df.to_csv("2023_place_canvas_20072023.csv", index=False)
