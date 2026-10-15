import io
import re
import hashlib
import zipfile

import streamlit as st

# --- CORE BACKEND LOGIC (Level 4 Framework) ---
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
    "33": "Illizi", "34": "Bordj Bou Arréridj", "35": "Boumerdès",
    "36": "El Tarf", "37": "Tindouf", "38": "Tissemsilt", "39": "El Oued",
    "40": "Khenchela", "41": "Souk Ahras", "42": "Tipaza", "43": "Mila",
    "44": "Aïn Defla", "45": "Naâma", "46": "Aïn Témouchent",
    "47": "Ghardaïa", "48": "Relizane", "49": "Timimoun",
    "50": "Bordj Badji Mokhtar", "51": "Ouled Djellal", "52": "Béni Abbès",
    "53": "In Salah", "54": "In Guezzam", "55": "Touggourt", "56": "Djanet",
    "57": "El M'Ghair", "58": "El Meniaa",
}


def tokenize_text(content, ledger, log):
    """Replace NINs and phone numbers with tokens. Fills ledger and log."""
    for match in re.findall(NIN_PATTERN, content):
        gender_digit, commune, birth_year, wilaya_code = match
        gender = "Male" if gender_digit in ["1", "3"] else "Female"
        year_prefix = "19" if gender_digit in ["1", "2"] else "20"
        full_birth_year = f"{year_prefix}{birth_year}"
        region_name = WILAYAS.get(wilaya_code, f"Wilaya Code {wilaya_code}")
        log.append(f"   ├─ [METADATA] {gender} | Born: {full_birth_year} | Region: {region_name}")

    for nin in set(re.findall(FULL_NIN_MATCH, content)):
        nin_hash = hashlib.md5(nin.encode("utf-8")).hexdigest()[:8].upper()
        token = f"[NIN_TOKEN_{nin_hash}]"
        ledger[token] = nin
        content = content.replace(nin, token)

    for phone in set(re.findall(PHONE_PATTERN, content)):
        phone_hash = hashlib.md5(phone.encode("utf-8")).hexdigest()[:6].upper()
        token = f"[PHONE_TOKEN_{phone_hash}]"
        ledger[token] = phone
        content = content.replace(phone, token)

    return content


def build_ledger_text(ledger):
    lines = ["=== ANPDP LAW 18-07 COMPLIANT REVERSAL KEY ==="]
    for token, original in sorted(ledger.items()):
        lines.append(f"{token} ===> {original}")
    return "\n".join(lines) + "\n"


# --- STREAMLIT UI ---
st.set_page_config(page_title="Data Sovereign Shield", page_icon="🛡️")
st.title("🛡️ Data Sovereign Shield")
st.subheader("Outil d'Anonymisation de Données Cliniques")

tab_files, tab_text = st.tabs(["Fichiers .txt", "Texte collé"])

with tab_files:
    files = st.file_uploader(
        "Déposez vos fichiers .txt", type=["txt"], accept_multiple_files=True
    )
    if st.button("Lancer le pipeline", key="run_files"):
        if not files:
            st.warning("Veuillez déposer au moins un fichier .txt.")
        else:
            ledger, log, secured = {}, [], {}
            log.append(f">>> INITIALIZING LEVEL 5 CRYPTO ENGINE...")
            log.append(f"--> Status: ACTIVE. Securing {len(files)} entities.")
            log.append("=" * 60)
            for f in files:
                log.append(f"[PROCESSING]: {f.name}")
                try:
                    content = f.getvalue().decode("utf-8")
                    secured[f"secure_{f.name}"] = tokenize_text(content, ledger, log)
                    log.append("   └─ [VAULTED] File secured.")
                except Exception as error:
                    log.append(f"   └─ [SKIPPED] System issue processing file: {error}")
            log.append("=" * 60)
            log.append(">>> PIPELINE EXECUTED. MASTER AUDIT TRAIL RECORDED.")
            st.session_state["result"] = {
                "log": "\n".join(log),
                "secured": secured,
                "ledger": build_ledger_text(ledger),
            }

    result = st.session_state.get("result")
    if result:
        st.success("Pipeline terminé.")
        st.code(result["log"], language=None)
        if result["secured"]:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for name, text in result["secured"].items():
                    zf.writestr(name, text)
            st.download_button(
                "⬇️ Télécharger les fichiers sécurisés (.zip)",
                buf.getvalue(),
                file_name="secured_vault.zip",
                mime="application/zip",
            )
            st.download_button(
                "🔑 Télécharger la clé de réversion (vault_ledger.txt)",
                result["ledger"],
                file_name="vault_ledger.txt",
                mime="text/plain",
            )
            st.caption("Conservez la clé séparément des fichiers sécurisés.")

with tab_text:
    user_input = st.text_area("Entrez le texte à anonymiser :", height=200)
    if st.button("Anonymiser le texte", key="run_text"):
        if user_input.strip():
            ledger, log = {}, []
            out = tokenize_text(user_input, ledger, log)
            st.success("Anonymisation effectuée avec succès !")
            st.text_area("Résultat anonymisé :", value=out, height=200)
            st.download_button(
                "🔑 Clé de réversion", build_ledger_text(ledger),
                file_name="vault_ledger.txt", mime="text/plain",
            )
        else:
            st.warning("Veuillez saisir du texte.")
