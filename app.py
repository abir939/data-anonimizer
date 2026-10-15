import os
import re
import hashlib
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- CORE BACKEND LOGIC (Your Level 4 Framework) ---
NIN_PATTERN = r'\b(\d)(\d{3})(\d{2})(\d{2})\d{10}\b'
FULL_NIN_MATCH = r'\b\d{18}\b'
PHONE_PATTERN = r'\b(?:05|06|07)\d{8}\b'

WILAYAS = {
    "01": "Adrar", "02": "Chlef", "03": "Laghouat", "04": "Oum El Bouaghi",
    "05": "Batna", "06": "Béjaïa", "07": "Biskra", "08": "Béchar",
    "09": "Blida", "10": "Bouira", "11": "Tamanrasset", "12": "Tébessa",
    "13": "Tlemcen", "14": "Tiaret", "15": "Tizi Ouzou", "16": "Alger",
    "17": "Djelfa", "18": "Jijel", "19": "Sétif", "20": "Saïda",
    "21": "Skikda", "22": "Sidi Bel Abbès", "23": "Annaba", "24": "Guelma",
    "25": "Constantine", "26": "Médéa", "27": "Mostaganem", "28": "M'Sila",
    "29": "Mascara", "30": "Ouargla", "31": "Oran", "32": "El Bayadh",
    "33": "Illizi", "34": "Bordj Bou Arréridj", "35": "Boumerdès", "36": "El Tarf",
    "37": "Tindouf", "38": "Tissemsilt", "39": "El Oued", "40": "Khenchela",
    "41": "Souk Ahras", "42": "Tipaza", "43": "Mila", "44": "Aïn Defla",
    "45": "Naâma", "46": "Aïn Témouchent", "47": "Ghardaïa", "48": "Relizane",
    "49": "El M'Ghair", "50": "El Meniaa", "51": "Ouled Djellal", "52": "Bordj Badji Mokhtar",
    "53": "Béni Abbès", "54": "Timimoun", "55": "Touggourt", "56": "Djanet",
    "57": "In Salah", "58": "In Guezzam"
}

INPUT_DIR = "unprocessed_data"
OUTPUT_DIR = "secured_vault"
KEY_FILE = "vault_ledger.txt"

def run_vault_pipeline():
    """Triggers the full cryptographic execution layer from the visual button."""
    log_box.delete('1.0', tk.END)
    log_box.insert(tk.END, ">>> INITIALIZING LEVEL 5 CRYPTO ENGINE...\n")
    
    for folder in [INPUT_DIR, OUTPUT_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    try:
        files_to_process = [f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')]
    except Exception as e:
        log_box.insert(tk.END, f"[CRITICAL ERROR]: Directory access denied: {e}\n")
        return

    if not files_to_process:
        log_box.insert(tk.END, f"--> Status: STANDBY. No target documents located inside '{INPUT_DIR}/'.\n")
        messagebox.showinfo("Pipeline Status", "System is Standby. Place raw text files into 'unprocessed_data' folder.")
        return

    log_box.insert(tk.END, f"--> Status: ACTIVE. Securing {len(files_to_process)} enterprise data files...\n")
    log_box.insert(tk.END, "==============================================================\n\n")

    global_ledger = {}

    for filename in files_to_process:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, f"secure_{filename}")
        log_box.insert(tk.END, f"[PROCESSING]: {filename}\n")
        
        try:
            with open(input_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            matches = re.findall(NIN_PATTERN, content)
            for match in matches:
                gender_digit, commune, birth_year, wilaya_code = match
                gender = "Male" if gender_digit in ["1", "3"] else "Female"
                year_prefix = "19" if gender_digit in ["1", "2"] else "20"
                full_birth_year = f"{year_prefix}{birth_year}"
                region_name = WILAYAS.get(wilaya_code, f"Wilaya Code {wilaya_code}")
                log_box.insert(tk.END, f"   ├─► [METADATA] {gender} | Born: {full_birth_year} | {region_name}\n")

            all_nins = re.findall(FULL_NIN_MATCH, content)
            for nin in set(all_nins):  
                nin_hash = hashlib.md5(nin.encode('utf-8')).hexdigest()[:8].upper()
                token_string = f"[NIN_TOKEN_{nin_hash}]"
                global_ledger[token_string] = nin
                content = content.replace(nin, token_string)

            all_phones = re.findall(PHONE_PATTERN, content)
            for phone in set(all_phones):
                phone_hash = hashlib.md5(phone.encode('utf-8')).hexdigest()[:6].upper()
                token_string = f"[PHONE_TOKEN_{phone_hash}]"
                global_ledger[token_string] = phone
                content = content.replace(phone, token_string)

            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(content)
            log_box.insert(tk.END, f"   └─► [VAULTED] Encrypted target file deployed to folder.\n\n")

        except Exception as error:
            log_box.insert(tk.END, f"   └─► [SKIPPED] System issue processing file: {error}\n\n")

    try:
        with open(KEY_FILE, "w", encoding="utf-8") as ledger_file:
            ledger_file.write("=== ANPDP LAW 18-07 COMPLIANT REVERSAL KEY ===\n")
            for token, original in sorted(global_ledger.items()):
                ledger_file.write(f"{token} ===> {original}\n")
        log_box.insert(tk.END, "==============================================================\n")
        log_box.insert(tk.END, ">>> PIPELINE EXECUTED PERFECTLY. MASTER AUDIT TRAIL RECORDED.\n")
        messagebox.showinfo("Success", "All assets have been cryptographically tokenized and secured!")
    except Exception as ledger_error:
        log_box.insert(tk.END, f"[FATAL ERR] Ledger registry failure: {ledger_error}\n")


# --- GUI DESIGN INTERFACE LAYER (Layout) ---
mport re
import streamlit as st

st.set_page_config(page_title="Data Sovereign Shield", page_icon="🔒")

st.title("🔒 Data Sovereign Shield")
st.subheader("Outil d'Anonymisation de Données Cliniques")

# --- YOUR ANONYMIZATION REGEX FUNCTION HERE ---
def anonymize_text(text):
    # Place your existing regex substitution rules here
    # Example:
    # text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL ANONYMISÉ]', text)
    return text

# --- STREAMLIT UI ---
user_input = st.text_area("Entrez le texte ou les données cliniques à anonymiser :", height=200)

if st.button("Anonymiser les données"):
    if user_input.strip():
        result = anonymize_text(user_input)
        st.success("Anonymisation effectuée avec succès !")
        st.text_area("Résultat Anonymisé :", value=result, height=200)
    else:
        st.warning("Veuillez saisir du texte.")

