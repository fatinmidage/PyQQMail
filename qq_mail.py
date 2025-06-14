import imaplib
import email
from email.header import decode_header
import os
from typing import Optional, List, Dict
import yaml

class QQMail:
    def __init__(self, email_address: str = None, password: str = None):
        """
        初始化QQ邮箱客户端
        :param email_address: QQ邮箱地址（可选，如果不提供则从配置文件读取）
        :param password: 邮箱授权码（可选，如果不提供则从配置文件读取）
        """
        if email_address is None or password is None:
            config = self._load_config()
            self.email_address = email_address or config['email']['address']
            self.password = password or config['email']['password']
        else:
            self.email_address = email_address
            self.password = password
            
        self.imap_server = "imap.qq.com"
        self.imap_port = 993
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def _load_config(self) -> dict:
        """
        从配置文件加载邮箱配置
        :return: 配置信息字典
        """
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(config_path):
            raise FileNotFoundError("配置文件不存在，请先创建 config.yaml 文件")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config or 'email' not in config:
            raise ValueError("配置文件格式错误")
        
        if not config['email']['address'] or not config['email']['password']:
            raise ValueError("请在配置文件中填写邮箱地址和授权码")
        
        return config

    def connect(self) -> bool:
        """
        连接到QQ邮箱服务器
        :return: 连接是否成功
        """
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.connection.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def disconnect(self):
        """
        断开与邮箱服务器的连接
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
            except:
                pass
            finally:
                self.connection = None

    def get_mail_content(self, email_id: str) -> str:
        """
        获取邮件内容
        :param email_id: 邮件ID
        :return: 邮件内容
        """
        if not self.connection:
            raise Exception("未连接到邮箱服务器")

        try:
            _, msg_data = self.connection.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            content = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            content = part.get_payload(decode=True).decode()
                        except:
                            content = part.get_payload(decode=True).decode('gbk')
                        break
            else:
                try:
                    content = email_message.get_payload(decode=True).decode()
                except:
                    content = email_message.get_payload(decode=True).decode('gbk')
            
            return content
        except Exception as e:
            print(f"获取邮件内容失败: {str(e)}")
            return ""

    def get_mail_list(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """
        获取邮件列表
        :param folder: 邮件文件夹，默认为收件箱
        :param limit: 获取的邮件数量限制
        :return: 邮件列表
        """
        if not self.connection:
            raise Exception("未连接到邮箱服务器")

        try:
            self.connection.select(folder)
            _, messages = self.connection.search(None, "ALL")
            email_ids = messages[0].split()
            
            # 获取最新的limit封邮件
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            mail_list = []
            for email_id in email_ids:
                _, msg_data = self.connection.fetch(email_id, "(RFC822)")
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # 解析邮件主题
                subject = decode_header(email_message["Subject"])[0]
                if isinstance(subject[0], bytes):
                    subject = subject[0].decode(subject[1] or 'utf-8')
                else:
                    subject = subject[0]
                
                # 解析发件人
                from_addr = decode_header(email_message["From"])[0]
                if isinstance(from_addr[0], bytes):
                    from_addr = from_addr[0].decode(from_addr[1] or 'utf-8')
                else:
                    from_addr = from_addr[0]
                
                mail_list.append({
                    "id": email_id.decode(),
                    "subject": subject,
                    "from": from_addr,
                    "date": email_message["Date"]
                })
            
            return mail_list
        except Exception as e:
            print(f"获取邮件列表失败: {str(e)}")
            return []

def main():
    try:
        qq_mail = QQMail()
    except (FileNotFoundError, ValueError) as e:
        print(f"配置错误: {str(e)}")
        return
    
    if qq_mail.connect():
        print("登录成功！")
        
        # 获取最新的5封邮件
        mails = qq_mail.get_mail_list(limit=5)
        print("\n最新的5封邮件：")
        for mail in mails:
            print(f"\n主题: {mail['subject']}")
            print(f"发件人: {mail['from']}")
            print(f"日期: {mail['date']}")
            
            # 判断是否是交通银行信用卡中心的邮件
            if "交通银行信用卡中心" in mail['from']:
                print("\n发现交通银行信用卡中心的邮件，正在获取内容...")
                content = qq_mail.get_mail_content(mail['id'])
                print("\n邮件内容：")
                print("-" * 50)
                print(content)
                print("-" * 50)
            
            print("-" * 50)
        
        qq_mail.disconnect()
    else:
        print("登录失败！")

if __name__ == "__main__":
    main() 