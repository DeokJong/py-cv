import os
from PIL import Image

def find_and_remove_duplicates(folder_path):
    # 폴더 내의 모든 이미지 파일을 리스트로 가져오기
    image_files = sorted([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.png')])
    
    # 이미지 파일을 기준으로 비교
    i = 0
    while i < len(image_files):
        base_image_path = image_files[i]
        if not os.path.exists(base_image_path):
            i += 1
            continue  # 파일이 이미 삭제된 경우 넘어감
        
        with Image.open(base_image_path) as base_image:
            # base_image와 동일한 이미지를 찾고 삭제
            j = i + 1
            while j < len(image_files):
                compare_image_path = image_files[j]
                if compare_image_path is None or not os.path.exists(compare_image_path):
                    j += 1
                    continue  # 파일이 이미 삭제된 경우 넘어감

                with Image.open(compare_image_path) as compare_image:
                    # 이미지 크기가 다르면 바로 넘어감
                    if base_image.size != compare_image.size:
                        j += 1
                        continue
                    
                    # 픽셀 비교
                    if list(base_image.getdata()) == list(compare_image.getdata()):
                        os.remove(compare_image_path)  # 동일한 이미지 삭제
                        print(f"Deleted duplicate image: {compare_image_path}")
                        image_files[j] = None  # 이미지 리스트에서 제거
                j += 1
        
        # 삭제된 파일을 제거하고 리스트를 업데이트
        image_files = [file for file in image_files if file is not None]
        i += 1

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
    
    # 중복 이미지 찾기 및 제거
    find_and_remove_duplicates(folder_name)
