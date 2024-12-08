# -*- coding: utf-8 -*-
from pyhtml2pdf import converter

# HTML 템플릿
html_head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    <style>
        table {
            border: 2px solid; border-collapse: collapse; text-align: center; width: 650px; margin: 10px;
        }
        th, td { border: 1px solid; padding: 10px 5px; text-align: center; }
        th { background-color: lightgray; }
        body { margin: 30px; font-family: Arial, sans-serif; font-size:14px}
        h1 {font-size:24px}
        h2 {font-size:20px}
        img {height: 100px}
        .container {
            width: 100%;
            overflow: auto; /* 부모 요소 높이 자동 조정 */
        }
        .image {
            float: left; /* 왼쪽으로 정렬 */
            width: 50%;
            margin-right: 20px; /* 이미지와 텍스트 사이 여백 */
        }
        .text {
            float: left; /* 왼쪽으로 정렬 */
            width: 45%;
        }
        .caption {
            font-size: 10px;
        }
    </style>
</head>
<body>
<h1>CAN IDS REPORT</h1><h3>1. 차량 정보</h3>
<div style="display: flex; align-items: center;">
  <div style="flex: 1; text-align: center;">
      <img src="report/asset/logo.png" alt="Info Image">
  </div>
  <div style="flex: 2; line-height: 1.5; padding-left: 20px;">
      <p><b>차량 종류:</b> Avantte</p>
      <p><b>CAN ID 개수:</b> 56</p>
      <p><b>적용 유무 표시:</b> 유</p>
  </div>
</div>
"""
html_foot = """
</body>
</html>
"""

# 레포트 생성 함수
def generate_report(html_file_path, data_frames, sections, detailed_report):
    """
    HTML 레포트를 생성하고 저장하는 함수.

    Args:
        html_file_path (str): 생성할 HTML 파일의 경로.
        data_frames (list): DataFrame 목록.
        sections (list): 섹션 제목 목록.
    """
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(html_head)
        for section, df in zip(sections, data_frames):
            file.write('<hr style="border: none; height: 2px; background-color: gray; margin: 20px 0;">')
            file.write(f"<h2>{section}</h2>")
            if "기본 정보" in section:
                file.write("""
                            <div>
                           해당 차량의 CAN 프로토콜에 사용되는 CAN ID에 대한 기본적인 정보입니다.
                           <div class="caption">* 미측정: 초반 주기/비주기 판단 및 주기 측정을 위한 각 can id당 200개의 패킷 또는 40초 동안 한번도 사용되지 않은 ID입니다. <br>
                           * 비주기: 초반 주기/비주기 판단 및 주기 측정을 위한 각 can id당 200개의 패킷 또는 40초 동안 사용되었으나, CV(변동계수) 및 표준편차가 기준을 넘지 않아서 비주기로 판단된 ID입니다. 
                            </div></div>
                        """)
            elif "공격 감지 상태" in section:
                file.write("""
                            <div>
                           탐지된 공격에 대한 전반적인 정보입니다.
                           <div class="caption">
                           * label 1.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 2.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 3.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 4.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 5.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 6.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 7.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 8.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. </br>
                           * label 9.0: 해당 공격에 대한 아주 간략한 정보를 추가해 주세요. 
                           </div>
                            </div>
                        """)
            elif "SUMMARY" in section:

                                # 색상 매핑
                colors = ["#f39c12", "#8e44ad", "#3498db", "#2ecc71", "#e74c3c"]

                # 비율을 숫자로 변환
                df["탐지 비율 (%)"] = df["탐지 비율"].str.rstrip('%').astype(float)

                # conic-gradient 생성
                gradient_parts = []
                cumulative_percent = 0
                for index, row in df.iterrows():
                    start_percent = cumulative_percent
                    cumulative_percent += row["탐지 비율 (%)"]
                    gradient_parts.append(
                        f"{colors[index]} {start_percent}% {cumulative_percent}%"
                    )
                gradient_string = "background: conic-gradient( " + ",".join(gradient_parts) + ");"
                print(gradient_string)
                file.write(f"""
                            <div>
                                CAN IDS에서 탐지한 Attack Packet의 요약입니다. 각 공격의 종류와 비율, 갯수와 기준, 비율을 볼 수 있습니다. 
                            </div>
                            <div style="
                                width: 100px;
                                height: 100px;
                                border-radius: 50%;
                                {gradient_string}
                                margin: 50px auto;
                            "></div>
                            """)
            file.write(df.to_html(index=False, escape=False))
        # 상세 데이터 추가
        file.write('<hr style="border: none; height: 1px; background-color: gray; margin: 20px 0;">')
        file.write("<h2>Detailed Analysis</h2>")

        for i in range(len(detailed_report["title"])):
            
            file.write(f"""
                <p style="margin-top: 20px">
                    <span style="font-size: 16px; font-weight: bold;">{detailed_report["title"][i]}</span>
                    <span style="font-size: 14px; font-weight: normal;">    - detail: {detailed_report["subtitle"][i]}</span>
                </p>
                <div class="container">
                    <img src={detailed_report["img"][i]} alt="Rule set Image" class="image">
                    <div class="text">
                        <div>{detailed_report["describes"][i]}</div>
                    </div>
                </div>
                
                <hr style="border: none; height: 1px; background-color: lightgray; margin: 20px 0;">
            """)
            file.write(detailed_report["dataframe"][i].to_html(index=False, escape=False))

        file.write(html_foot)

# HTML을 PDF로 변환하는 함수
def html2pdf(file_path, pdf_path):
    try:
        if not file_path.endswith('.html'):
            print("Invalid file format. Only .html files are supported.")
            return False
        converter.convert(f'file://{file_path}', pdf_path)
        print(f"PDF saved at: {pdf_path}")
        return True
    except Exception as err:
        print(f"Error: {err}")
        return False
