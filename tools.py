import random

# --- SIMULASI DATABASE STATIS ---
# Di aplikasi nyata, ini akan mengambil data dari database SQL atau NoSQL
DB_TARIF = {
    "jakarta_bandung": {"origin": "GT Cikampek Utama", "destination": "GT Pasteur", "price": 60000},
    "jakarta_semarang": {"origin": "GT Cikampek Utama", "destination": "GT Kalikangkung", "price": 352000},
    "surabaya_malang": {"origin": "GT Waru", "destination": "GT Singosari", "price": 30500}
}

DB_REST_AREA = {
    "cipali": [
        {"km": 102, "direction": "A (Jakarta ke Cirebon)", "facilities": ["SPBU", "Masjid", "Restoran", "Toilet"]},
        {"km": 101, "direction": "B (Cirebon ke Jakarta)", "facilities": ["Masjid", "Restoran", "Toilet"]}
    ],
    "merak": [
        {"km": 43, "direction": "A (Jakarta ke Merak)", "facilities": ["SPBU", "Restoran"]}
    ]
}

DB_DARURAT = {
    "jasa_marga": "14080",
    "cipali": "0260-7600-600",
    "jagorawi": "021-841-3632"
}

# --- DEFINISI TOOLS / FUNGSI ---

def get_toll_tariff(origin: str, destination: str) -> str:
    """
    Mencari tarif tol berdasarkan kota asal dan tujuan.
    """
    print(f"Tool Dipanggil: get_toll_tariff({origin}, {destination})")
    
    # Logika pencarian sederhana (disimulasikan)
    key = f"{origin.lower()}_{destination.lower()}"
    reverse_key = f"{destination.lower()}_{origin.lower()}"
    
    if key in DB_TARIF:
        data = DB_TARIF[key]
        return f"Tarif tol dari {data['origin']} ke {data['destination']} adalah Rp {data['price']:,}."
    elif reverse_key in DB_TARIF:
        data = DB_TARIF[reverse_key]
        return f"Tarif tol dari {data['origin']} ke {data['destination']} adalah Rp {data['price']:,}."
    else:
        return f"Maaf, Sobat. Saya tidak menemukan data tarif untuk rute {origin} ke {destination}."

def get_traffic_info(location: str) -> str:
    """
    Mendapatkan informasi lalu lintas real-time di lokasi tertentu (misal: nama tol atau KM).
    """
    print(f"Tool Dipanggil: get_traffic_info({location})")
    
    # --- SIMULASI API REAL-TIME ---
    # Di aplikasi nyata, ini akan memanggil API eksternal (misal: Google Maps, Waze)
    conditions = ["lancar", "padat merayap", "macet total akibat kecelakaan", "ramai lancar"]
    selected_condition = random.choice(conditions)
    
    return f"Update lalu lintas terkini di {location}: Kondisi saat ini terpantau {selected_condition}."

def get_rest_area_info(toll_road: str, facility_needed: str = None) -> str:
    """
    Mencari informasi rest area di ruas tol tertentu, bisa difilter berdasarkan fasilitas.
    """
    print(f"Tool Dipanggil: get_rest_area_info({toll_road}, {facility_needed})")
    
    if toll_road.lower() not in DB_REST_AREA:
        return f"Maaf, data untuk rest area di Tol {toll_road} belum tersedia."
        
    areas = DB_REST_AREA[toll_road.lower()]
    results = []
    
    for area in areas:
        if facility_needed:
            if facility_needed.lower() in [f.lower() for f in area["facilities"]]:
                results.append(area)
        else:
            results.append(area)
            
    if not results:
        return f"Tidak ditemukan rest area di Tol {toll_road} dengan fasilitas {facility_needed}."
    
    # Format output
    output = f"Berikut rest area di Tol {toll_road}:\n"
    for res in results:
        facilities_str = ", ".join(res['facilities'])
        output += f"- KM {res['km']} (Arah {res['direction']}): {facilities_str}\n"
    return output

def get_emergency_number(toll_road: str = "jasa_marga") -> str:
    """
    Memberikan nomor darurat call center tol. Defaultnya adalah Jasa Marga.
    """
    print(f"Tool Dipanggil: get_emergency_number({toll_road})")
    
    number = DB_DARURAT.get(toll_road.lower(), DB_DARURAT["jasa_marga"])
    if toll_road.lower() == "jasa_marga":
        return f"Nomor darurat Call Center Jasa Marga (umum) adalah {number}."
    else:
        return f"Nomor darurat untuk Tol {toll_road} adalah {number}. Jika tidak tersambung, hubungi call center umum Jasa Marga di {DB_DARURAT['jasa_marga']}."