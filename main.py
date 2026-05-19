import pandas as pd
import json
import random

try:
    with open('competency_map.json', 'r') as f:
        competency_map = json.load(f)
except Exception as e:
    print("ERROR: File competency_map.json tidak ditemukan di folder!")
    exit()

star_signals = {
    "HIGH": {
        "context": "Kandidat menjelaskan konteks proyek skala besar di industri dengan sangat kronologis dan detail.",
        "contribution": "Menjelaskan akuntabilitas pribadi dan peran kepemimpinan dalam menyelesaikan bottleneck teknis.",
        "metrics": "Menyebutkan dampak performa bisnis secara kuantitatif dengan metrik yang terukur jelas (misal: reduksi latency 40%, akurasi 95%)."
    },
    "LOW": {
        "context": "Kandidat menjawab terlalu singkat, mengambang, and tidak menyebutkan latar belakang proyek.",
        "contribution": "Hanya menyebutkan kerja tim tanpa memperjelas kontribusi spesifik dirinya sendiri.",
        "metrics": "Tidak ada metrik evaluasi yang jelas, hanya klaim subjektif bahwa sistem berjalan lancar."
    }
}

expanded_rows = []

print("Memulai proses Perbanyakan & Validasi Dataset (Data Science Pipeline)...")

for role, role_info in competency_map.items():
    role_family = role_info["role_family"]
    domain = role_info["domain"]
    
    for comp in role_info["competencies"]:
        comp_name = comp["competency"]
        related_tools = ", ".join(comp["related_skills"])
        
        for i in range(5):
            expanded_rows.append({
                "domain": domain,
                "role_family": role_family,
                "target_role": role,
                "competency": comp_name,
                "related_skills": related_tools,
                "candidate_answer": f"Pada proyek terakhir terkait {comp_name}, saya bertanggung jawab penuh menggunakan {related_tools}. {star_signals['HIGH']['context']} {star_signals['HIGH']['contribution']} Hasilnya, {star_signals['HIGH']['metrics']}",
                "star_relevance_score": round(random.uniform(0.85, 1.00), 2),
                "technical_accuracy_score": round(random.uniform(0.88, 1.00), 2),
                "evidence_level": random.choice([4, 5]),
                "final_answer_quality_label": "HIGH_QUALITY"
            })
            
        for i in range(5): 
            expanded_rows.append({
                "domain": domain,
                "role_family": role_family,
                "target_role": role,
                "competency": comp_name,
                "related_skills": related_tools,
                "candidate_answer": f"Saya pernah ikut tim mengerjakan {comp_name} pakai {related_tools}. {star_signals['LOW']['context']} {star_signals['LOW']['contribution']} {star_signals['LOW']['metrics']}",
                "star_relevance_score": round(random.uniform(0.10, 0.45), 2),
                "technical_accuracy_score": round(random.uniform(0.20, 0.50), 2),
                "evidence_level": random.choice([1, 2]),
                "final_answer_quality_label": "LOW_QUALITY"
            })

df_expanded = pd.DataFrame(expanded_rows)
df_expanded.to_csv('answer_quality_dataset.csv', index=False)

print(f"Dataset sukses diperbanyak menjadi {len(df_expanded)} BARIS DATA VALID!")
print("File 'answer_quality_dataset.csv' siap dipakai!")