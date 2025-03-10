from datetime import datetime
import re
import uuid
import os
import shutil

def parseIndex():
    # HTML 파일 경로
    file_path = './AppleJournalEntries/index.html'

    # 결과를 저장할 배열
    href_entries = []

    try:
        # HTML 파일을 raw text로 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        
        # 정규표현식으로 href="Entries/~~~.html" 패턴 찾기
        pattern = r'href="(Entries/[^"]+\.html)"'
        matches = re.findall(pattern, raw_text)

        for match in matches:
            unique_id = str(uuid.uuid4()).replace('-', '')  # 고유 UUID 생성
            href_entries.append([match, unique_id])
        href_entries.reverse()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return href_entries

def parseEntry(entry_path, i):
    # HTML 파일 경로
    file_path = f'./AppleJournalEntries/{entry_path[0]}'

    # 결과를 저장할 딕셔너리
    entry = {
        'id': entry_path[1],
        'title': '',
        'date': '',
        'content': '',
        'photos': ''
    }

    try:
        # HTML 파일을 raw text로 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        
        # title 찾기
        title_pattern = r'<div class="title">(.+)</div>'
        title_match = re.search(title_pattern, raw_text)
        if title_match:
            entry['title'] = title_match.group(1)

        # date 찾기
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        date_match = re.search(date_pattern, entry_path[0])
        if date_match:
            string_date = date_match.group(1)
            unix_date = str(round(datetime.strptime(string_date, '%Y-%m-%d').timestamp()) + i) + '000'
            entry['date'] = unix_date

        # content 찾기
        content_pattern = r"<div class='bodyText'>(.+)</div>"
        # strip html tags
        content_match = re.search(content_pattern, raw_text, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            content = re.sub(r'<[^>]+>', '', content).strip('\n')
            entry['content'] = content

        # photos 찾기
        photos_pattern = r'<img src="([^"]+)"'
        photos_matches = re.findall(photos_pattern, raw_text)
        photos = []
        for photo in photos_matches:
            photos.append(photo)
        entry['photos'] = photos

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return entry


if __name__ == '__main__':
    # user input timezone -12~14

    while True:
        timezone = input('Enter your timezone offset. (-12 ~ 14)'
        "\n.5 accepted. For example, enter 5.5 if your timezone is '+05:30' : ")
        try:
            timezone = float(timezone)
            if timezone < -12 or timezone > 14:
                raise ValueError
            if timezone % 0.5 != 0:
                raise ValueError
            break
        except ValueError:
            print('Invalid input. Please enter a valid timezone offset.')

    hours = int(abs(timezone))
    minutes = int((abs(timezone) % 1) * 60)
    sign = '+' if timezone >= 0 else '-'
    timezone_str = f"{sign}{hours:02d}:{minutes:02d}"

    with open('backup_empty_template.xml', 'r', encoding='utf-8') as file:
        empty_xml = file.read()
    
    unix_timestamp = str(round(datetime.now().timestamp()))
    path = f'./Backup_{unix_timestamp}'
    os.makedirs(path, exist_ok=True)
    os.makedirs(f'{path}/media/photo', exist_ok=True)
    
    entries_data = ""
    attachments_data = ""
    
    entries = parseIndex()
    for i, entry in enumerate(entries):
        entry_data = parseEntry(entry, i)
        
        # 엔트리 데이터 준비
        entries_data += f'<r>\n\t<uid>{entry_data["id"]}</uid>\n\t<date>{entry_data["date"]}</date>\n\t<tz_offset>{timezone_str}</tz_offset>\n\t<title>{entry_data["title"]}</title>\n\t<text>{entry_data["content"]}</text>\n\t<folder_uid></folder_uid>\n\t<location_uid></location_uid>\n\t<tags></tags>\n\t<primary_photo_uid></primary_photo_uid>\n\t<weather_temperature>0</weather_temperature>\n\t<weather_icon></weather_icon>\n\t<weather_description></weather_description>\n\t<mood></mood>\n</r>\n'
        
        # 첨부 파일 데이터 준비 및 복사
        for i, photo in enumerate(entry_data['photos']):
            attachments_data += f'<r>\n\t<uid>{os.path.basename(photo).split(".")[0].replace("-", "").lower()}</uid>\n\t<entry_uid>{entry_data["id"]}</entry_uid>\n\t<type>photo</type>\n\t<filename>{os.path.basename(photo.replace("../",""))}</filename>\n\t<position>{i + 1}</position>\n</r>\n'
            
            source = f'./AppleJournalEntries/{photo.replace("../", "")}'
            destination = f'{path}/media/photo/{os.path.basename(photo.replace("../", ""))}'
            shutil.copy(source, destination)
    
    # 태그 사이에 데이터 삽입
    modified_xml = empty_xml.replace('<table name="diaro_entries">\n</table>', f'<table name="diaro_entries">\n{entries_data}</table>')
    modified_xml = modified_xml.replace('<table name="diaro_attachments">\n</table>', f'<table name="diaro_attachments">\n{attachments_data}</table>')
    
    # 수정된 XML 저장
    with open(f'./Backup_{unix_timestamp}/DiaroBackup.xml', 'w', encoding='utf-8') as file:
        file.write(modified_xml)

    # XML과 media 폴더 압축
    shutil.make_archive(path, 'zip', path)

    print(f'Backup complete. Import this zip file in Diarium, as "Diaro" backup. : {path}.zip')