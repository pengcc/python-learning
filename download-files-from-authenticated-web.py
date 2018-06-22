import requests
import os

from bs4 import BeautifulSoup


LOGIN_URL = 'https://www.YOUR_PAPE.com/login.html'
username = 'YOUR_USERNAME'
password = 'YOUR_PASS'
URL = "https://www.YOUR_PAPE.com/example"
URL_base = "https://www.YOUR_PAPE.com/"

# find out your parameters used for auth
payload = {
    'user': username,
    'pass': password
}

auth_data = {
    'param1': 'YOUR_VALUE1',
    'param12': 'YOUR_VALUE2',
    'param3': 'YOUR_VALUE3'
}
# Update payload
payload.update(auth_data)

def get_container_list_by_soup(html_text, _parser="html.parser"):
    """
    parse the html by beautifulsoup
    :param: _parser: string
    :param: html_text: html text that needs to be parsed
    :return: matched elements list
    """
    bf_html = BeautifulSoup(html_text, _parser)
    # see my html in example.html
    # change the parameters, get your target element list
    ele_list = bf_html.find_all('div', class_='tt_content')
    return ele_list


def download_and_save_file(session_requests, directory, file_url, file_name):
    with session_requests.get(file_url, headers=dict(referer=file_url)) as response, open(
            os.path.join(directory, file_name), 'wb') as out_file:
        out_file.write(response.content)


def main():
    file_list = []
    session_requests = requests.session()

    # Perform login
    session_requests.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

    # Scrape url
    res_text = session_requests.get(URL, headers=dict(referer=URL)).text
    tree = get_container_list_by_soup(res_text)
    for leaf in tree:
        tem = {}
        directory = leaf.select_one('div.csc-header').text
        tem['directory'] = directory
        items = []
        download_items = leaf.select('.user-interhomesintern-pi1 > .download-item')
        # create a directory
        os.makedirs(directory, exist_ok=True)

        for item in download_items:
            target = item.select_one('.download-item-name > a')
            link = target['href']
            name = target.text
            items.append({'link': link, 'name': name})

            download_and_save_file(session_requests, directory, URL_base+link, name)

        tem['items'] = items
        file_list.append(tem)

    # print result
    # print(filter_result)


if __name__ == '__main__':
    main()

