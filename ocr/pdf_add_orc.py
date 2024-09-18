import easyocr
import fitz  # PyMuPDF
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
import numpy as np
import gc

# OCR 리더 생성
reader = easyocr.Reader(['ko', 'en'])  # 한글과 영어 텍스트 인식


def extract_text_from_pdf(pdf_path):
    """
    PDF 파일의 각 페이지에서 이미지를 추출하고 OCR로 텍스트를 추출합니다.
    """
    extracted_texts = []
    pdf_document = fitz.open(pdf_path)

    for page_num in tqdm(range(len(pdf_document)), desc="Extracting Text", unit="page"):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # 이미지 스트리밍 방식으로 처리
        img_data = io.BytesIO(pix.tobytes())
        img = Image.open(img_data)
        
        # 이미지 압축: 그레이스케일로 변환
        img = img.convert("L")
        
        # PIL 이미지를 numpy 배열로 변환
        img_np = np.array(img)

        # OCR로 텍스트 추출
        results = reader.readtext(img_np)
        page_text = " ".join([result[1] for result in results])
        extracted_texts.append(page_text)

        # 중간 데이터 삭제
        del img_np
        del img_data
        gc.collect()  # 가비지 컬렉션 수행

    return extracted_texts


def create_blank_text_pdf(output_file, text, position, page_size=letter):
    """
    빈 PDF에 텍스트를 삽입하여 생성합니다.
    """
    c = canvas.Canvas(output_file, pagesize=page_size)
    c.setFont("Helvetica", 12)
    c.drawString(position[0], position[1], text)
    c.showPage()
    c.save()


def overlay_text_on_pdf(pdf_path, output_pdf_path, extracted_texts, positions):
    """
    기존 PDF에 추출된 텍스트를 덮어씌워 새로운 PDF를 생성합니다.
    """
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(pdf_path)

    for page_num in tqdm(range(len(pdf_reader.pages)), desc="Overlaying Text", unit="page"):
        page = pdf_reader.pages[page_num]

        # 각 페이지에 대한 빈 텍스트 PDF 생성
        blank_text_pdf = f"temp_page_{page_num}.pdf"
        create_blank_text_pdf(blank_text_pdf, extracted_texts[page_num], positions[page_num])

        # 기존 페이지에 텍스트 덮어쓰기
        pdf_writer.add_page(page)

    with open(output_pdf_path, 'wb') as f:
        pdf_writer.write(f)


def main():
    pdf_path = "input.pdf"  # 처리할 PDF 경로
    output_pdf_path = "output_pdf_file.pdf"  # 출력될 PDF 경로

    # PDF에서 텍스트 추출
    extracted_texts = extract_text_from_pdf(pdf_path)

    # 텍스트가 삽입될 위치 (임의로 설정)
    positions = [(100, 500)] * len(extracted_texts)  # 페이지마다 동일한 위치에 텍스트 삽입

    # 추출된 텍스트를 기반으로 PDF 생성
    overlay_text_on_pdf(pdf_path, output_pdf_path, extracted_texts, positions)

    print(f"PDF 파일이 성공적으로 생성되었습니다: {output_pdf_path}")


if __name__ == "__main__":
    main()
