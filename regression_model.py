import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import joblib # Untuk menyimpan model

# --- 1. Mengimpor Data dari File Output Gold Layer ---

try:

    gold_df_output = pd.read_parquet('D:\RANGGA\Projek Pipeline ABD\imports_aggregated.parquet')
except FileNotFoundError:
    print("Error: File output Gold Layer tidak ditemukan. Pastikan path dan nama file sudah benar.")
    print("Harap jalankan pipeline ETL untuk menghasilkan output Gold Layer terlebih dahulu.")
    exit()
except Exception as e:
    print(f"Terjadi error saat membaca file: {e}")
    exit()


print("Data dari Gold Layer berhasil diimpor:")
print(gold_df_output.head())
print("\nInformasi Data:")
gold_df_output.info()


required_columns = ['reporterDesc', 'cmdDesc', 'refYear', 'total_cifvalue']
missing_cols = [col for col in required_columns if col not in gold_df_output.columns]
if missing_cols:
    print(f"Error: Kolom berikut tidak ditemukan dalam dataset Gold Layer: {missing_cols}")
    exit()


# --- 2. Feature Engineering untuk Time Series ---

df_engineered = gold_df_output.sort_values(by=['reporterDesc', 'cmdDesc', 'refYear']).reset_index(drop=True)


df_engineered['cifvalue_lag1'] = df_engineered.groupby(['reporterDesc', 'cmdDesc'])['total_cifvalue'].shift(1)
df_engineered['cifvalue_lag2'] = df_engineered.groupby(['reporterDesc', 'cmdDesc'])['total_cifvalue'].shift(2)

df_engineered['cifvalue_diff1'] = df_engineered.groupby(['reporterDesc', 'cmdDesc'])['total_cifvalue'].diff(1)

df_engineered['cifvalue_ma2'] = df_engineered.groupby(['reporterDesc', 'cmdDesc'])['total_cifvalue'].shift(1).rolling(window=2, min_periods=1).mean()

y = df_engineered['total_cifvalue']
X = df_engineered[['reporterDesc', 'cmdDesc', 'refYear', 'cifvalue_lag1', 'cifvalue_lag2', 'cifvalue_diff1', 'cifvalue_ma2']]

original_indices_count = len(X)
X = X.dropna()
y = y.loc[X.index] 

print(f"\nJumlah baris sebelum dropna (akibat lag/transformasi): {original_indices_count}")
print(f"Jumlah baris setelah dropna: {len(X)}")

if X.empty:
    print("\nTidak ada data yang tersisa setelah membuat fitur lag dan menghapus NaN.")
    print("Ini bisa terjadi jika setiap kelompok (reporterDesc, cmdDesc) hanya memiliki sedikit entri tahun.")
    print("Model regresi memerlukan setidaknya beberapa titik data per kelompok untuk membuat fitur lag yang valid.")
    exit()

print("\nData setelah Feature Engineering (X):")
print(X.head())
print("\nTarget Variable (y):")
print(y.head())


# --- 3. Pra-pemrosesan Data ---

numerical_features = ['refYear', 'cifvalue_lag1', 'cifvalue_lag2', 'cifvalue_diff1', 'cifvalue_ma2']
categorical_features = ['reporterDesc', 'cmdDesc']


numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), 
    ('scaler', StandardScaler())
])


categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ],
    remainder='passthrough' 
)

# --- 4. Pemisahan Data (Time-Series Aware Split) ---

if X['refYear'].nunique() < 2:
    print("Tidak cukup variasi tahun untuk melakukan split train/test berdasarkan tahun terakhir.")
    print("Menggunakan train_test_split biasa dengan shuffle=False.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
else:
    latest_year = X['refYear'].max()
    X_train = X[X['refYear'] < latest_year]
    y_train = y[X_train.index]
    X_test = X[X['refYear'] == latest_year]
    y_test = y[X_test.index]

if X_train.empty or X_test.empty:
    print("Data latih atau data uji kosong setelah split. Tidak cukup data atau variasi tahun.")
    print("Menggunakan train_test_split biasa dengan shuffle=False sebagai fallback.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    if X_train.empty or X_test.empty:
        print("Fallback train_test_split juga menghasilkan set kosong. Hentikan.")
        exit()


print(f"\nUkuran data latih: {X_train.shape}, Ukuran data uji: {X_test.shape}")


# --- 5. Pembuatan dan Pelatihan Model Regresi ---

model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True, n_jobs=-1)) # n_jobs=-1 untuk menggunakan semua core
])

print("\nMelatih model Random Forest Regressor...")
try:
    model_pipeline.fit(X_train, y_train)
    print(f"Model OOB Score: {model_pipeline.named_steps['regressor'].oob_score_:.4f}")
except Exception as e:
    print(f"Error saat melatih model: {e}")
    exit()

# --- 6. Evaluasi Model ---
if not X_test.empty:
    print("\nMelakukan prediksi pada data uji...")
    y_pred = model_pipeline.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nMetrik Evaluasi Model pada Data Uji:")
    print(f"  Mean Squared Error (MSE)     : {mse:.2f}")
    print(f"  Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"  Mean Absolute Error (MAE)    : {mae:.2f}")
    print(f"  R-squared (R2) Score         : {r2:.4f}")

    # --- 7. Visualisasi Hasil Prediksi (Opsional) ---
    plt.figure(figsize=(12, 7))
    plt.scatter(y_test.values, y_pred, alpha=0.7, edgecolors='w', linewidth=0.5, label='Prediksi vs Aktual')

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Ideal (y=x)')
    plt.xlabel("Nilai Aktual (total_cifvalue)")
    plt.ylabel("Nilai Prediksi (total_cifvalue)")
    plt.title("Perbandingan Nilai Aktual vs. Prediksi pada Data Uji")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("\nData uji kosong, evaluasi dan visualisasi dilewati.")


# --- 9. Membuat Prediksi untuk Masa Depan (Contoh) ---

def prepare_future_data(df_full, last_known_year, future_target_year):
    future_X_list = []

    latest_data_known = df_full[df_full['refYear'] == last_known_year]



    for _, row in latest_data_known.iterrows():

        val_lag1 = row['total_cifvalue'] 
        

        prev_year_data = df_full[
            (df_full['reporterDesc'] == row['reporterDesc']) &
            (df_full['cmdDesc'] == row['cmdDesc']) &
            (df_full['refYear'] == last_known_year - 1)
        ]
        val_lag2 = prev_year_data['total_cifvalue'].iloc[0] if not prev_year_data.empty else np.nan 

        diff1 = val_lag1 - val_lag2 if pd.notna(val_lag1) and pd.notna(val_lag2) else np.nan
        ma2_values = []
        if pd.notna(val_lag1): ma2_values.append(val_lag1)
        if pd.notna(val_lag2): ma2_values.append(val_lag2)
        ma2 = np.mean(ma2_values) if ma2_values else np.nan


        future_X_list.append({
            'reporterDesc': row['reporterDesc'],
            'cmdDesc': row['cmdDesc'],
            'refYear': future_target_year,
            'cifvalue_lag1': val_lag1,
            'cifvalue_lag2': val_lag2,
            'cifvalue_diff1': diff1,
            'cifvalue_ma2': ma2
        })
    return pd.DataFrame(future_X_list) if future_X_list else pd.DataFrame()

if not df_engineered.empty:
    last_data_year = df_engineered['refYear'].max()
    year_to_predict = last_data_year + 1

    future_X_df = prepare_future_data(df_engineered, last_data_year, year_to_predict)

    if not future_X_df.empty:
        print(f"\nData input untuk prediksi masa depan ({year_to_predict}):")
        print(future_X_df.head())

        for col in numerical_features:
            if col in future_X_df.columns and future_X_df[col].isnull().any():
                future_X_df[col] = future_X_df[col].fillna(median_val)
                print(f"Mengisi NaN di kolom '{col}' pada data masa depan dengan median: {median_val}")


        future_predictions = model_pipeline.predict(future_X_df)
        future_X_df['predicted_cifvalue_next_year'] = future_predictions

        print(f"\nHasil prediksi nilai impor untuk tahun {year_to_predict}:")
        print(future_X_df[['reporterDesc', 'cmdDesc', 'refYear', 'predicted_cifvalue_next_year']])
    else:
        print(f"\nTidak dapat menyiapkan data input untuk prediksi masa depan ({year_to_predict}).")
else:
    print("\nTidak ada data yang diproses untuk prediksi masa depan.")


print("\nPengembangan model regresi dari output Gold Layer selesai.")