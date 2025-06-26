import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge

# 🔹 Kodun bulunduğu klasörü ayarla
base_dir = os.path.dirname(os.path.abspath(__file__))

# 🔹 Veri dosyasını oku (aynı klasörde olmalı)
excel_path = os.path.join(base_dir, "oznitelikler.xlsx")
df = pd.read_excel(excel_path)
df_clean = df.dropna(subset=['Ortalama_Sıcaklık'])

X_vars = [col for col in df_clean.columns if col not in ['Country', 'Ortalama_Sıcaklık']]
df_all = df_clean.dropna(subset=X_vars)

results = []

# 🔁 Ülke bazlı Ridge regresyon tahmini
for country in df_all['Country'].unique():
    cdf = df_all[df_all['Country'] == country]
    if len(cdf) < 5 or 2013 not in cdf['Year'].values:
        continue

    X = pd.get_dummies(cdf[X_vars], drop_first=False)
    y = cdf['Ortalama_Sıcaklık']

    model = Pipeline([
        ('scale', StandardScaler()),
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('ridge', Ridge(alpha=1.0))
    ])
    model.fit(X, y)

    row_2013 = cdf[cdf['Year'] == 2013].copy()
    row_2013['Year'] = 2100

    X_pred = pd.get_dummies(row_2013[X_vars], drop_first=False)
    for col in X.columns:
        if col not in X_pred.columns:
            X_pred[col] = 0
    X_pred = X_pred[X.columns]

    tahmin_2100 = model.predict(X_pred)[0]
    gercek_2013 = row_2013['Ortalama_Sıcaklık'].values[0]
    fark = tahmin_2100 - gercek_2013

    if fark < 1:
        risk = 'Düşük Risk'
    elif fark < 1.5:
        risk = 'Orta Risk'
    elif fark < 2:
        risk = 'Yüksek Risk'
    else:
        risk = 'Çok Yüksek Risk'

    results.append({
        'Ülke': country,
        'Sıcaklık_2013': round(gercek_2013, 2),
        'Tahmini_Sıcaklık_2100': round(tahmin_2100, 2),
        'Fark (°C)': round(fark, 2),
        'Risk Seviyesi': risk
    })

df_results_updated = pd.DataFrame(results).sort_values(by="Fark (°C)", ascending=False)
kita_bilgisi = df_all[['Country', 'Kıta']].drop_duplicates()
df_results_with_kita = df_results_updated.merge(kita_bilgisi, left_on='Ülke', right_on='Country', how='left').drop(columns='Country')

# 🔁 Risk özeti oluştur ve sıralama yap
risk_kita_summary = df_results_with_kita.groupby(['Risk Seviyesi', 'Kıta'], observed=True)['Ülke'].count().reset_index()
risk_kita_summary.columns = ['Risk Seviyesi', 'Kıta', 'Ülke Sayısı (Kıtaya Göre)']

risk_total_summary = df_results_with_kita.groupby('Risk Seviyesi', observed=True)['Ülke'].count().reset_index()
risk_total_summary.columns = ['Risk Seviyesi', 'Toplam Ülke Sayısı']

final_summary = pd.merge(risk_kita_summary, risk_total_summary, on='Risk Seviyesi', how='left')
risk_order = ['Çok Yüksek Risk', 'Yüksek Risk', 'Orta Risk', 'Düşük Risk']
final_summary['Risk Seviyesi'] = pd.Categorical(final_summary['Risk Seviyesi'], categories=risk_order, ordered=True)
final_summary = final_summary.sort_values(by='Risk Seviyesi')

# 📁 Excel'e kaydet
excel_out = os.path.join(base_dir, "Kod_Cıktısı.xlsx")
with pd.ExcelWriter(excel_out, engine="openpyxl") as writer:
    df_results_with_kita.to_excel(writer, sheet_name="Tahmin Sonuçları", index=False)
    final_summary.to_excel(writer, sheet_name="Risk Özeti", index=False)

# 📊 Grafik 1: Kıta Bazlı Risk Dağılımı
plt.figure(figsize=(12, 6))
sns.countplot(data=df_results_with_kita, x='Risk Seviyesi', hue='Kıta', order=risk_order)
plt.title("Kıta Bazlı Risk Dağılımı (2100 Tahminlerine Göre)")
plt.ylabel("Ülke Sayısı")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "kita_risk_dagilimi_bar.png"))

# 📊 Grafik 2: Histogram
plt.figure(figsize=(10, 6))
plt.hist(df_results_with_kita["Fark (°C)"], bins=15, color='orange', edgecolor='black')
plt.title("2100 Sıcaklık Artışı Dağılımı (Histogram)")
plt.xlabel("Sıcaklık Artışı (°C)")
plt.ylabel("Ülke Sayısı")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "sicaklik_artisi_histogram.png"))

# 📊 Grafik 3: En Fazla Isınacak İlk 10 Ülke
top10 = df_results_with_kita.sort_values(by='Fark (°C)', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top10, y='Ülke', x='Fark (°C)', hue='Ülke', palette='Reds_r', legend=False)
plt.title("En Fazla Isınacak İlk 10 Ülke (2100 Tahmini)")
plt.xlabel("Sıcaklık Artışı (°C)")
plt.ylabel("Ülke")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "en_fazla_isinacak_10_ulke.png"))
