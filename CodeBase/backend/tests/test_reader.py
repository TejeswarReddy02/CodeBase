from app.repository.reader import read_repository


repository_path = r"C:\FinalYearProject\CodeBase\data\repositories\laptop-price-predictor"

files = read_repository(repository_path)

print(f"Files found: {len(files)}")

for file in files:
    print(
        file["file_path"],
        "|",
        file["language"],
        "|",
        file["line_count"],
        "lines"
    )