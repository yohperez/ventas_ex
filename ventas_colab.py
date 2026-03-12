# ============================================================
#  SOLUCIÓN EJERCICIO TABLA VENTAS — Google Colab
#  Ejecuta cada celda en orden
# ============================================================

# ── CELDA 1: Instalar librerías necesarias ───────────────────
# !pip install openpyxl matplotlib pandas --quiet


# ── CELDA 2: Importaciones ───────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from io import StringIO


# ── CELDA 3: Cargar el CSV ───────────────────────────────────
# Opción A – subir el archivo manualmente en Colab:
# from google.colab import files
# uploaded = files.upload()
# df = pd.read_csv(list(uploaded.keys())[0])

# Opción B – datos directamente (del archivo ventas.csv):
csv_raw = """fecha,producto,precio,unidades
2024-01-01,Camiseta,20,5
2024-01-02,Pantalón,30,2
2024-01-03,Camiseta,20,3
2024-01-04,Zapatillas,50,1
2024-01-05,Pantalón,30,4
2024-01-06,Sudadera,35,2
2024-01-07,Zapatillas,50,2
2024-01-08,Camiseta,20,6
2024-01-09,Pantalón,30,1
2024-01-10,Sudadera,35,3"""

df = pd.read_csv(StringIO(csv_raw), parse_dates=["fecha"])
print("✅ Dataset cargado:")
print(df.to_string(index=False))


# ── CELDA 4: Crear columna TOTAL ─────────────────────────────
df["total"] = df["precio"] * df["unidades"]
print("\n✅ Columna 'total' creada (precio × unidades):")
print(df[["fecha", "producto", "precio", "unidades", "total"]].to_string(index=False))


# ── CELDA 5: Estadísticas — PROMEDIO, SUMA, MÁX ─────────────
promedio = df["total"].mean()
suma     = df["total"].sum()
maximo   = df["total"].max()

print("\n📊 Estadísticas de la columna TOTAL:")
print(f"   PROMEDIO : {promedio:.2f} €")
print(f"   SUMA     : {suma:.2f} €")
print(f"   MÁX      : {maximo:.2f} €")


# ── CELDA 6: Filtro — productos con ingresos > 100 € ─────────
df_filtrado = df[df["total"] > 100].copy()
print(f"\n✅ Filtro aplicado: productos con total > 100 €  ({len(df_filtrado)} filas)")
print(df_filtrado[["fecha", "producto", "total"]].to_string(index=False))


# ── CELDA 7: Extraer el mes en texto desde la columna fecha ──
MESES_ES = {
    1:"enero", 2:"febrero", 3:"marzo",    4:"abril",
    5:"mayo",  6:"junio",   7:"julio",    8:"agosto",
    9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}
df["mes"] = df["fecha"].dt.month.map(MESES_ES)
print("\n✅ Columna 'mes' en texto:")
print(df[["fecha", "mes", "producto", "total"]].to_string(index=False))


# ── CELDA 8: Dataset final como CSV ─────────────────────────
csv_output = "ventas_procesado.csv"
df.to_csv(csv_output, index=False, encoding="utf-8-sig")
print(f"\n✅ Dataset guardado como '{csv_output}'")
# Para descargarlo en Colab descomenta la línea siguiente:
# files.download(csv_output)


# ── CELDA 9: Tabla dinámica — ingresos totales por producto y mes
pivot = df.pivot_table(
    values="total",
    index="producto",
    columns="mes",
    aggfunc="sum",
    fill_value=0
)

# Ordenar columnas por mes calendario
orden_meses = [m for m in MESES_ES.values() if m in pivot.columns]
pivot = pivot[orden_meses]

# Añadir columna de total general por producto
pivot["TOTAL"] = pivot.sum(axis=1)

print("\n📊 Tabla dinámica — Ingresos totales por producto y mes (€):")
print(pivot.to_string())


# ── CELDA 10: Gráfico de barras ──────────────────────────────
pivot_chart = pivot.drop(columns="TOTAL")   # sin columna TOTAL para el gráfico

fig, ax = plt.subplots(figsize=(11, 6))

# Colores por barra
colors = ["#1F4E79", "#2E75B6", "#5BA3D0", "#A8D1F0"]
pivot_chart.plot(
    kind="bar",
    ax=ax,
    color=colors[:len(pivot_chart.columns)],
    edgecolor="white",
    linewidth=0.6,
    width=0.7
)

# Formato del eje Y en euros
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} €"))

# Etiquetas de valor sobre cada barra
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f €", fontsize=7.5,
                 padding=3, color="#333333")

# Estética general
ax.set_title("Ingresos Totales por Producto y Mes", fontsize=14,
             fontweight="bold", pad=16, color="#1F4E79")
ax.set_xlabel("Producto", fontsize=11, labelpad=8)
ax.set_ylabel("Ingresos (€)", fontsize=11, labelpad=8)
ax.set_xticklabels(pivot_chart.index, rotation=0, fontsize=10)
ax.legend(title="Mes", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, linestyle="--", alpha=0.5)
ax.set_axisbelow(True)
ax.set_facecolor("#F7FBFF")
fig.patch.set_facecolor("white")

plt.tight_layout()
plt.savefig("grafico_ventas.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Gráfico guardado como 'grafico_ventas.png'")


# ── CELDA 11: Resumen final ──────────────────────────────────
print("\n" + "="*55)
print("  RESUMEN FINAL")
print("="*55)
print(f"  Total de registros          : {len(df)}")
print(f"  Productos únicos            : {df['producto'].nunique()}")
print(f"  Período                     : {df['fecha'].min().date()} → {df['fecha'].max().date()}")
print(f"  PROMEDIO de ingresos/venta  : {promedio:.2f} €")
print(f"  SUMA total de ingresos      : {suma:.2f} €")
print(f"  MÁX ingreso en una venta    : {maximo:.2f} €")
print(f"  Ventas con total > 100 €    : {len(df_filtrado)}")
print("="*55)
