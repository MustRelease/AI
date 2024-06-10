def load_dotenv(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # 주석 처리된 줄과 빈 줄을 건너뛰기
            if line.startswith('#') or not line.strip():
                continue
            # 키=값 형태의 줄을 파싱
            key, value = line.strip().split('=', 1)
            return value
