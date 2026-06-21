# pylint: disable=import-outside-toplevel

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco...
    """
    import os
    import glob
    import pandas as pd

    # 1. Buscar y leer todos los archivos comprimidos
    rutas_archivos = glob.glob("files/input/*.zip")
    
    lista_dfs = [pd.read_csv(archivo, compression='zip') for archivo in rutas_archivos]
    df = pd.concat(lista_dfs, ignore_index=True)

    # ==========================================
    # 2. Procesar client.csv
    # ==========================================
    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client["credit_default"] = client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    # ==========================================
    # 3. Procesar campaign.csv
    # ==========================================
    campaign = df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome"]].copy()
    
    campaign["previous_outcome"] = campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    
    meses_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", 
        "may": "05", "jun": "06", "jul": "07", "aug": "08", 
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    mes_formateado = df["month"].str.lower().map(meses_map)
    dia_formateado = df["day"].astype(str).str.zfill(2)
    
    # Aquí está el nombre correcto que exige la prueba automática
    campaign["last_contact_date"] = "2022-" + mes_formateado + "-" + dia_formateado

    # ==========================================
    # 4. Procesar economics.csv
    # ==========================================
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # ==========================================
    # 5. Exportar los resultados
    # ==========================================
    os.makedirs("files/output", exist_ok=True)
    
    client.to_csv("files/output/client.csv", index=False)
    campaign.to_csv("files/output/campaign.csv", index=False)
    economics.to_csv("files/output/economics.csv", index=False)

    return

if __name__ == "__main__":
    clean_campaign_data()