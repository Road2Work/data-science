import json

with open('competencies.json', 'r', encoding='utf-8') as file:
    matriks_peran = json.load(file)

print("=" * 60)
print("MATRIKS KOMPETENSI PROYEK ASLI BERHASIL DIOLAH!")
print("=" * 60 + "\n")

for nama_role, detail in matriks_peran.items():
    if nama_role == "system_metadata":
        continue
        
    print(f"ROLE: {nama_role.upper()}")
    print(f"   Rumpun Peran : {detail['role_family']}")
    print(f"   Domain       : {detail['domain']}")
    print(f"   Kompetensi   :")
    
    for indeks, comp in enumerate(detail['competencies'], 1):
        print(f"      {indeks}. {comp['competency']} (Bobot Score: {comp['weight']})")
        print(f"         Skills Inti: {', '.join(comp['related_skills'])}")
    print("-" * 60)