import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def classify_air_quality(daily_mean, weekly_mean, overall_mean):
    """
    Classifica la qualità dell'aria per ogni giorno in base ai valori medi di O3.

    Parametri
    ---------
    daily_mean : pandas.Series
        Valori medi di O3 per ogni giorno.
    weekly_mean : pandas.Series
        Valori medi di O3 per ogni settimana.
    overall_mean : float
        Valore medio complessivo di O3 per il dataset.

    Restituisce
    -----------
    results : list di dict
        Lista con i risultati della classificazione per ogni giorno.
    """
    results = []
    for day, value in daily_mean.items():
        week = pd.Timestamp(day).isocalendar().week
        day_mean = value
        week_mean = weekly_mean[week]
        if day_mean < week_mean and day_mean < overall_mean:
            quality = 'Buona'
        else:
            quality = 'Scarsa'
        results.append({'date': day, 'o3_mean': day_mean, 'quality': quality})
    return results


def get_peak_hours(df):
    """
    Trova le 3 ore di picco di O3 previsto per ogni giorno.

    Parametri
    ---------
    df : pandas.DataFrame
        DataFrame con le colonne 'Day', 'Hour' e 'O3_pred'.

    Restituisce
    -----------
    peak_hours : pandas.DataFrame
        DataFrame con le 3 ore di picco e il valore previsto di O3 per ogni giorno.
    """
    peak_hours = (
        df.groupby('Day')
        .apply(lambda x: x.nlargest(3, 'O3_pred')[['Hour', 'O3_pred']])
    )
    return peak_hours


def classification_report_o3(y_test, y_pred, overall_mean):
    """
    Stampa il classification report per la previsione di O3 (sopra/sotto la media).

    Parametri
    ---------
    y_test : pandas.Series o numpy.ndarray
        Valori reali di O3.
    y_pred : numpy.ndarray
        Valori previsti di O3.
    overall_mean : float
        Valore medio complessivo di O3 per la soglia.

    Restituisce
    -----------
    None
    """
    y_test_class = (y_test > overall_mean).astype(int)
    y_pred_class = (y_pred > overall_mean).astype(int)
    print(classification_report(y_test_class, y_pred_class, target_names=['Basso O3', 'Alto O3']))


def weekly_o3_classification_report(X_weekly, y_weekly, overall_mean):
    """
    Stampa il classification report per la previsione settimanale di O3 (sopra/sotto la media globale).

    Parametri
    ---------
    X_weekly : pandas.DataFrame
        Medie settimanali di NOx, GT, NO2.
    y_weekly : pandas.Series
        Medie settimanali di O3.
    overall_mean : float
        Media globale di O3.

    Restituisce
    -----------
    None
    """
    lr = LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(X_weekly, y_weekly, test_size=0.2, random_state=42)
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    y_test_class = (y_test > overall_mean).astype(int)
    y_pred_class = (y_pred > overall_mean).astype(int)
    print("Classification report regressione lineare settimanale O3 (sopra/sotto media globale):")
    print(classification_report(y_test_class, y_pred_class, target_names=['Basso O3', 'Alto O3']))


df = pd.read_csv('airquality_parsed.csv', parse_dates=['DateTime'])

# Calcola le medie
daily_mean = df.groupby(df['DateTime'].dt.date)['O3'].mean()
weekly_mean = df.groupby(df['DateTime'].dt.isocalendar().week)['O3'].mean()
overall_mean = df['O3'].mean()

# Classificazione per ogni giorno
results = classify_air_quality(daily_mean, weekly_mean, overall_mean)

# Prepara le feature e il target
features = ['NOx', 'GT', 'NO2']
target = 'O3'

# Prevedi O3 con Random Forest
rf = RandomForestRegressor()
X = df[features]
y = df[target]
rf.fit(X, y)
df['O3_pred'] = rf.predict(X)

# Trova le 3 ore di picco di O3 per ogni giorno
df['Hour'] = df['DateTime'].dt.hour
df['Day'] = df['DateTime'].dt.date

peak_hours = get_peak_hours(df)
#print(peak_hours)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# Discretizza O3 in classi: 1 se sopra la media complessiva, 0 se sotto
overall_mean = y.mean()
y_test_class = (y_test > overall_mean).astype(int)
y_pred_class = (y_pred > overall_mean).astype(int)

classification_report_o3(y_test, y_pred, overall_mean)

# Calcola medie giornaliere
df['Day'] = df['DateTime'].dt.date
daily_means = df.groupby('Day')[['NOx', 'GT', 'NO2', 'O3']].mean()
daily_means['Week'] = pd.to_datetime(daily_means.index).isocalendar().week

# Calcola medie settimanali
weekly_means = daily_means.groupby('Week')[['NOx', 'GT', 'NO2', 'O3']].mean()
X_weekly = weekly_means[['NOx', 'GT', 'NO2']]
y_weekly = weekly_means['O3']

# Regressione lineare e classification report
weekly_o3_classification_report(X_weekly, y_weekly, overall_mean)




