# work in progress, but they seem to block the requests very fast, so prob not worth it


import requests
from bs4 import BeautifulSoup
import re

urls = [
"https://spys.one/en/free-proxy-list/US/", "https://spys.one/en/free-proxy-list/RU/", "https://spys.one/en/free-proxy-list/SG/",
"https://spys.one/en/free-proxy-list/MX/", "https://spys.one/en/free-proxy-list/DE/", "https://spys.one/en/free-proxy-list/GB/",
"https://spys.one/en/free-proxy-list/BR/", "https://spys.one/en/free-proxy-list/HK/", "https://spys.one/en/free-proxy-list/FR/",
"https://spys.one/en/free-proxy-list/JP/", "https://spys.one/en/free-proxy-list/CO/", "https://spys.one/en/free-proxy-list/IR/",
"https://spys.one/en/free-proxy-list/TH/", "https://spys.one/en/free-proxy-list/FI/", "https://spys.one/en/free-proxy-list/ZA/",
"https://spys.one/en/free-proxy-list/EC/", "https://spys.one/en/free-proxy-list/ID/", "https://spys.one/en/free-proxy-list/IN/",
"https://spys.one/en/free-proxy-list/PH/", "https://spys.one/en/free-proxy-list/VN/", "https://spys.one/en/free-proxy-list/BD/",
"https://spys.one/en/free-proxy-list/EG/", "https://spys.one/en/free-proxy-list/KR/", "https://spys.one/en/free-proxy-list/TR/",
"https://spys.one/en/free-proxy-list/CN/", "https://spys.one/en/free-proxy-list/VE/", "https://spys.one/en/free-proxy-list/CL/",
"https://spys.one/en/free-proxy-list/NL/", "https://spys.one/en/free-proxy-list/ES/", "https://spys.one/en/free-proxy-list/DO/",
"https://spys.one/en/free-proxy-list/PE/", "https://spys.one/en/free-proxy-list/AR/", "https://spys.one/en/free-proxy-list/CA/",
"https://spys.one/en/free-proxy-list/PL/", "https://spys.one/en/free-proxy-list/UA/", "https://spys.one/en/free-proxy-list/PK/",
"https://spys.one/en/free-proxy-list/KH/", "https://spys.one/en/free-proxy-list/AU/", "https://spys.one/en/free-proxy-list/TW/",
"https://spys.one/en/free-proxy-list/KE/", "https://spys.one/en/free-proxy-list/IT/", "https://spys.one/en/free-proxy-list/MY/",
"https://spys.one/en/free-proxy-list/SE/", "https://spys.one/en/free-proxy-list/LY/", "https://spys.one/en/free-proxy-list/IQ/",
"https://spys.one/en/free-proxy-list/HU/", "https://spys.one/en/free-proxy-list/CZ/", "https://spys.one/en/free-proxy-list/GT/",
"https://spys.one/en/free-proxy-list/HN/", "https://spys.one/en/free-proxy-list/PY/", "https://spys.one/en/free-proxy-list/NP/",
"https://spys.one/en/free-proxy-list/YE/", "https://spys.one/en/free-proxy-list/SA/", "https://spys.one/en/free-proxy-list/BG/",
"https://spys.one/en/free-proxy-list/NG/", "https://spys.one/en/free-proxy-list/IE/", "https://spys.one/en/free-proxy-list/PS/",
"https://spys.one/en/free-proxy-list/RS/", "https://spys.one/en/free-proxy-list/RO/", "https://spys.one/en/free-proxy-list/KZ/",
"https://spys.one/en/free-proxy-list/AE/", "https://spys.one/en/free-proxy-list/CH/", "https://spys.one/en/free-proxy-list/AL/",
"https://spys.one/en/free-proxy-list/LB/", "https://spys.one/en/free-proxy-list/GR/", "https://spys.one/en/free-proxy-list/SK/",
"https://spys.one/en/free-proxy-list/UZ/", "https://spys.one/en/free-proxy-list/QA/", "https://spys.one/en/free-proxy-list/TZ/",
"https://spys.one/en/free-proxy-list/BY/", "https://spys.one/en/free-proxy-list/BO/", "https://spys.one/en/free-proxy-list/PR/",
"https://spys.one/en/free-proxy-list/AF/", "https://spys.one/en/free-proxy-list/LV/", "https://spys.one/en/free-proxy-list/AT/",
"https://spys.one/en/free-proxy-list/LT/", "https://spys.one/en/free-proxy-list/BE/", "https://spys.one/en/free-proxy-list/NO/",
"https://spys.one/en/free-proxy-list/AM/", "https://spys.one/en/free-proxy-list/IL/", "https://spys.one/en/free-proxy-list/GE/",
"https://spys.one/en/free-proxy-list/HR/", "https://spys.one/en/free-proxy-list/MD/", "https://spys.one/en/free-proxy-list/MM/",
"https://spys.one/en/free-proxy-list/XK/", "https://spys.one/en/free-proxy-list/KG/", "https://spys.one/en/free-proxy-list/UY/",
"https://spys.one/en/free-proxy-list/BA/", "https://spys.one/en/free-proxy-list/CR/", "https://spys.one/en/free-proxy-list/PT/",
"https://spys.one/en/free-proxy-list/MN/", "https://spys.one/en/free-proxy-list/ME/", "https://spys.one/en/free-proxy-list/GH/",
"https://spys.one/en/free-proxy-list/DK/", "https://spys.one/en/free-proxy-list/PA/", "https://spys.one/en/free-proxy-list/CD/",
"https://spys.one/en/free-proxy-list/CM/", "https://spys.one/en/free-proxy-list/MK/", "https://spys.one/en/free-proxy-list/NZ/",
"https://spys.one/en/free-proxy-list/UG/", "https://spys.one/en/free-proxy-list/SV/", "https://spys.one/en/free-proxy-list/MG/",
"https://spys.one/en/free-proxy-list/ZW/", "https://spys.one/en/free-proxy-list/MW/", "https://spys.one/en/free-proxy-list/SI/",
"https://spys.one/en/free-proxy-list/SY/", "https://spys.one/en/free-proxy-list/NI/", "https://spys.one/en/free-proxy-list/LK/",
"https://spys.one/en/free-proxy-list/AO/", "https://spys.one/en/free-proxy-list/JO/", "https://spys.one/en/free-proxy-list/AZ/",
"https://spys.one/en/free-proxy-list/NA/", "https://spys.one/en/free-proxy-list/EE/", "https://spys.one/en/free-proxy-list/BW/",
"https://spys.one/en/free-proxy-list/OM/", "https://spys.one/en/free-proxy-list/IS/", "https://spys.one/en/free-proxy-list/ZM/",
"https://spys.one/en/free-proxy-list/MZ/", "https://spys.one/en/free-proxy-list/TN/", "https://spys.one/en/free-proxy-list/CY/",
"https://spys.one/en/free-proxy-list/LU/", "https://spys.one/en/free-proxy-list/SC/", "https://spys.one/en/free-proxy-list/RW/",
"https://spys.one/en/free-proxy-list/DZ/", "https://spys.one/en/free-proxy-list/MV/", "https://spys.one/en/free-proxy-list/LA/",
"https://spys.one/en/free-proxy-list/BJ/", "https://spys.one/en/free-proxy-list/TJ/", "https://spys.one/en/free-proxy-list/GN/",
"https://spys.one/en/free-proxy-list/TL/", "https://spys.one/en/free-proxy-list/CU/", "https://spys.one/en/free-proxy-list/MO/",
"https://spys.one/en/free-proxy-list/MU/", "https://spys.one/en/free-proxy-list/BH/", "https://spys.one/en/free-proxy-list/BI/",
"https://spys.one/en/free-proxy-list/MA/", "https://spys.one/en/free-proxy-list/CI/", "https://spys.one/en/free-proxy-list/GQ/",
"https://spys.one/en/free-proxy-list/BT/", "https://spys.one/en/free-proxy-list/SO/", "https://spys.one/en/free-proxy-list/SS/",
"https://spys.one/en/free-proxy-list/KW/", "https://spys.one/en/free-proxy-list/SN/", "https://spys.one/en/free-proxy-list/TD/",
"https://spys.one/en/free-proxy-list/HT/", "https://spys.one/en/free-proxy-list/BF/", "https://spys.one/en/free-proxy-list/GA/",
"https://spys.one/en/free-proxy-list/ML/", "https://spys.one/en/free-proxy-list/YT/", "https://spys.one/en/free-proxy-list/MT/",
"https://spys.one/en/free-proxy-list/KY/", "https://spys.one/en/free-proxy-list/VG/", "https://spys.one/en/free-proxy-list/BZ/",
"https://spys.one/en/free-proxy-list/SH/", "https://spys.one/en/free-proxy-list/FJ/", "https://spys.one/en/free-proxy-list/TM/",
"https://spys.one/en/free-proxy-list/GY/", "https://spys.one/en/free-proxy-list/CG/", "https://spys.one/en/free-proxy-list/TG/",
"https://spys.one/en/free-proxy-list/ET/", "https://spys.one/en/free-proxy-list/BB/", "https://spys.one/en/free-proxy-list/SL/",
"https://spys.one/en/free-proxy-list/PG/", "https://spys.one/en/free-proxy-list/GU/", "https://spys.one/en/free-proxy-list/LS/",
"https://spys.one/en/free-proxy-list/JM/", "https://spys.one/en/free-proxy-list/TT/", "https://spys.one/en/free-proxy-list/GM/",
"https://spys.one/en/free-proxy-list/WS/", "https://spys.one/en/free-proxy-list/SD/", "https://spys.one/en/free-proxy-list/AD/",
"https://spys.one/en/free-proxy-list/SZ/", "https://spys.one/en/free-proxy-list/BM/", "https://spys.one/en/free-proxy-list/DJ/",
"https://spys.one/en/free-proxy-list/MQ/", "https://spys.one/en/free-proxy-list/SR/", "https://spys.one/en/free-proxy-list/VI/",
"https://spys.one/en/free-proxy-list/GI/", "https://spys.one/en/free-proxy-list/MR/", "https://spys.one/en/free-proxy-list/TV/",
"https://spys.one/en/free-proxy-list/LR/", "https://spys.one/en/free-proxy-list/VU/", "https://spys.one/en/free-proxy-list/SX/",
]

total_proxies = []
for url in urls:
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    # antoher user agent 
    #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'zip
    }
    #payload = 'xx00=&xpp=5&xf1=0&xf2=0&xf4=0&xf5=0'

    print(f"Scraping URL: {url}")
    response = requests.request("GET", url, headers=headers)
    print(f"Response status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    with open("spys.html", "w") as f:
        f.write(soup.prettify())

    # Find the <script type="text/javascript"> tag and extract its content
    script_tag = soup.find("script", {"type": "text/javascript"})
    if script_tag:
        script_content = script_tag.string
        #print(f"Script content: {script_content}")
        pairs = script_content.split(';')
        
        # Initialize an empty dictionary
        result_dict = {}
        
        for pair in pairs:
            if '^' in pair:
                key, value = pair.split('=')
                result_dict[key] = value[0]
        
        # Print the resulting dictionary
        #print('\n\n')
        #print(f"Resulting dictionary: {result_dict}")
    else:
        print(f"Script tag not found in {url}")
        continue

    def extract_proxies(soup):
        proxies = []
        pattern = re.compile(r'\(\w+\^\w+\)(\+\(\w+\^\w+\))+')

        for tr_tag in soup.find_all('tr', class_=['spy1xx', 'spy1x']):
            ip_tag = tr_tag.find('font', class_='spy14')
            if ip_tag:
                proxy_ip = ip_tag.contents[0].strip()
                script_tag = ip_tag.find_next('script')
                script_content = script_tag.string if script_tag else ''
                match = pattern.search(script_content)
                if match:
                    script_pattern = match.group()
                    #print(f"IP: {proxy_ip}, Script Pattern: {script_pattern.strip()}") # this prints "IP: 181.233.93.88, Script Pattern: (u1m3t0^g7e5)+(v2t0m3^m3a1)+(u1m3t0^g7e5)+(v2t0m3^m3a1)"

                    # now we need to match up the script pattern with the result_dict to get the port, remember that each (<port num>^<port num>) is two keys in the result_dict
                    port = ''
                    #print
                    for key in script_pattern.replace("(",'').replace(")",'').split('+'):
                        v, k = key.split('^')
                        port += result_dict[v]

                    proxies.append(f"{proxy_ip}:{port}")
        return proxies

    proxies_list = extract_proxies(soup)
    print(f"Found a total of {len(proxies_list)} proxies")
    for proxy in proxies_list:
        total_proxies.append(proxy)