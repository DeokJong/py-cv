import os
from PIL import Image

# 현재 디렉토리의 모든 파일을 검색하여 .gif 파일만 선택
current_directory = '.'
gif_files = [file for file in os.listdir(current_directory) if file.endswith('.gif')]

for gif_file in gif_files:
    # GIF 파일 열기
    gif = Image.open(gif_file)
    
    # GIF 파일 이름에서 확장자를 제거하고 폴더 이름 생성
    folder_name = os.path.splitext(gif_file)[0]
    
    # 폴더 생성 (이미 존재하면 예외 처리로 넘어감)
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        pass
    
    # 각 프레임을 추출하고 폴더에 저장
    frame_number = 0
    while True:
        try:
            gif.seek(frame_number)  # 프레임 이동
            frame = gif.copy()  # 현재 프레임 복사
            frame.save(os.path.join(folder_name, f'frame_{frame_number}.png'))  # 프레임을 PNG로 저장
            frame_number += 1
        except EOFError:
            break  # 더 이상 프레임이 없을 때 중단
