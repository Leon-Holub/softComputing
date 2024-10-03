import helpFunctions as hf
import matplotlib.pyplot as plt

'''
Zobrazte graf s četnostmi žánrů her mezi lety 1990 (včetně) a 2000 (vyjma).
'''


def task1(filteredData):
    genres = filteredData['Genre'].value_counts()

    plt.figure(figsize=(10, 5))
    genres.plot(kind='bar')
    plt.title('Četnost žánrů her mezi lety 1990 a 1999')
    plt.xlabel('Žánr')
    plt.ylabel('Počet her')
    plt.tight_layout()
    plt.savefig('charts/graf1.png')
    plt.show()


'''Najděte korelační koeficient mezi prodeji v NA a EU. Hodnota: 0.767727'''


def task2(df):
    corr = df['NA_Sales'].corr(df['EU_Sales'])
    print(corr)
    return corr


'''Zobrazte v grafu korelační koeficient (NA vs. EU) v jednotlivých letech od roku 1985 po rok 2010'''


def task3(filteredData):
    corr = filteredData.groupby('Year').apply(lambda x: x['NA_Sales'].corr(x['EU_Sales']))
    plt.figure(figsize=(10, 5))
    plt.scatter(corr.index, corr.values)
    plt.title('Korelační koeficient (NA vs. EU) v jednotlivých letech od roku 1985 po rok 2010')
    plt.xlabel('Rok')
    plt.ylabel('Korelační koeficient')
    plt.tight_layout()
    plt.savefig('charts/graf2.png')
    plt.show()


'''Jaké jsou základní statistické údaje rozdílu v prodejích NA a EU pro žánr "Sports", u minima a maxima zjistěte o jaké hry se jedná - minimum (-4.95, FIFA 16), maximum (12.47, Wii Sports), průměr (0.130648), směrodatná odchylka (0.548157)'''


def task4(data):
    filteredData = data[data['Genre'] == 'Sports']
    diff = filteredData['NA_Sales'] - filteredData['EU_Sales']
    print('Min:', diff.min(), filteredData.loc[diff.idxmin(), 'Name'])
    print('Max:', diff.max(), filteredData.loc[diff.idxmax(), 'Name'])
    print('Průměr:', diff.mean())
    print('Odchylka:', diff.std())


'''Koláčový graf pro zobrazení dominance platforem v prodejích her, pod 2% spojit do jedné others(Pocet platforem)'''


def task5(data):
    allPlatforms = data['Platform'].value_counts(normalize=True)
    platforms = allPlatforms[allPlatforms >= 0.02]
    platformsWithLess = allPlatforms[allPlatforms < 0.02]
    platforms['Ostatní - {}'.format(len(platformsWithLess))] = platformsWithLess.sum()
    platforms = platforms[platforms >= 0.02]

    plt.figure(figsize=(10, 5))
    platforms.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Dominance platforem v prodejích her')
    plt.tight_layout()
    plt.savefig('charts/graf3.png')
    plt.show()


'''Nejlépe prodávajících se top 10 her celkově. Součet prodejů všech verzí hry. + graf'''


def task6(data):
    top10 = data.groupby('Name')['Global_Sales'].sum().nlargest(10)

    plt.figure(figsize=(10, 5))
    top10.plot(kind='bar')
    plt.title('Top 10 nejlépe prodávajících se her celkově')
    plt.xlabel('Hra')
    plt.ylabel('Celkové prodeje')
    plt.tight_layout()
    plt.savefig('charts/graf4.png')
    plt.show()


'''Pro každý rok mezi 2000 a 2010 vypočítejte medián rozdílu v prodejích mezi Severní Amerikou (NA) a Japonskem (JP) a zjistěte, ve kterém roce byl tento rozdíl největší a nejmenší.'''


def task7(data):
    filteredData = hf.get_games_from_to(data, 2000, 2010)
    diff = filteredData.groupby('Year').apply(lambda x: x['NA_Sales'].median() - x['JP_Sales'].median())
    print('Největší rozdíl:', diff.idxmax(), diff.max())
    print('Nejmenší rozdíl:', diff.idxmin(), diff.min())


'''Zjisti, jaký podíl prodejů mají žánry her vydávaných na platformě "PlayStation" ve srovnání s "X-BOX. Vytvoř graf, který porovnává rozložení žánrů na "PlayStation" s celkovým rozložením žánrů napříč všemi platformami.'''
def task8(data):
    ps = data[data['Platform'].str.contains('PS')]['Genre'].value_counts(normalize=True)
    xBox = data[data['Platform'].str.contains('XB')]['Genre'].value_counts(normalize=True)

    plt.figure(figsize=(10, 5))
    ps.plot(kind='bar', color='blue', alpha=0.5, label='PlayStation')
    xBox.plot(kind='bar', color='green', alpha=0.5, label='X-BOX')
    plt.title('Rozložení žánrů na PlayStation vs. X-BOX')
    plt.xlabel('Žánr')
    plt.ylabel('Podíl')
    plt.legend()
    plt.tight_layout()
    plt.savefig('charts/graf5.png')
    plt.show()

if __name__ == '__main__':
    df = hf.read_data('data/vgsales.csv')
    task1(hf.get_games_from_to(df, 1990, 1999))
    task2(df)
    task3(hf.get_games_from_to(df, 1985, 2010))
    task4(df)
    task5(df)
    task6(df)
    task7(df)
    task8(df)