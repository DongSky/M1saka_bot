import re
import os
import requests
import pathlib
ACCOUNT = "your id, not username or email"
PASSWORD = "your password"
class PixivGet(object):
    def __init__(self):
        if not os.path.isdir("pixiv"):
            os.makedirs("pixiv")
        self.account = ACCOUNT
        self.password = PASSWORD
        self.login_headers = {
            "Referer":"https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0",
            "Host":"accounts.pixiv.net",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive"
        }
        self.return_to = "http://www.pixiv.net/"
        self.post_key = []
        self.base_url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
        self.sess = requests.Session()
        self.login()
    def login(self):
        login_html = self.sess.get(self.base_url)
        pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)
        result = re.search(pattern, login_html.text)
        self.post_key = result.group(1)
        login_data = {
            "pixiv_id":self.account,
            "password":self.password,
            "post_key":self.post_key,
            "return_to":self.return_to
        }
        self.sess.post(self.login_url, data=login_data, headers=self.login_headers)
    def img_download(self,img_link,page_link):
        header = {
            "Referer":page_link,
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0"
        }
        try:
            download_path = str(pathlib.Path(os.getcwd()) / "pixiv" / img_link.split("/")[-1])
            if not os.path.exists(download_path):
                img = self.sess.get(img_link, headers=header)
                with open(download_path, "wb") as f:
                    f.write(img.content)
                    f.close()
            return download_path
        except Exception as e:
            print(e)
            return "ERIRI"
    def pixiv_auto_get(self,ID):
        pic_index_link = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s"%ID
        headers = {
            "Referer":"https://www.pixiv.net",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0",
        }
        pic_html = self.sess.get(pic_index_link)
        single_image_pattern = re.compile('<div class="_illust_modal.*?<img alt="(.*?)".*?data-src="(.*?)".*?</div>', re.S)
        single_img_result = re.search(single_image_pattern, pic_html.text)
        if single_img_result:
            img_name = single_img_result.group(1)
            img_source_url = single_img_result.group(2)
            pic_path = self.img_download(img_source_url, pic_index_link)
            if not pic_path.startswith("ERIRI"):
                return [pic_path]
            else:
                return None
        else:
            pic_index_link = pic_index_link.replace("medium", "manga")
            pic_html = self.sess.get(pic_index_link)
            total_num_pattern = re.compile('<span class="total">(\d*)</span></div>', re.S)
            total_num = re.search(total_num_pattern, pic_html.text)
            if total_num:
                total_path = []
                img_url_pattern = re.compile('<div class="item-container.*?<img src=".*?".*?data-src="(.*?)".*?</div>', re.S)
                url_result = re.findall(img_url_pattern, pic_html.text)
                try:
                    for item in url_result:
                        pic_path = self.img_download(img_source_url, pic_index_link)
                        total_path.append(pic_path)
                    return total_path
                except Exception as e:
                    print("===")
                    print(e)
                    return None
            else:
                return None
def pixiv_auto_get(pixiv_id):
    pixiv = PixivGet()
    pixiv.login()
    return pixiv.pixiv_auto_get(str(pixiv_id))
if __name__=="__main__":
    pixiv = PixivGet()
    pixiv.login()
    pixiv.pixiv_auto_get("65637109")
