import imaplib
import email
from email.header import decode_header
from typing import Optional, List, Dict
from config import load_config

class QQMail:
    def __init__(self, email_address: str = None, password: str = None):
        """
        初始化QQ邮箱客户端
        :param email_address: QQ邮箱地址（可选，如果不提供则从配置文件读取）
        :param password: 邮箱授权码（可选，如果不提供则从配置文件读取）
        """
        if email_address is None or password is None:
            config = load_config()
            self.email_address = email_address or config['email']['address']
            self.password = password or config['email']['password']
        else:
            self.email_address = email_address
            self.password = password
            
        self.imap_server = "imap.qq.com"
        self.imap_port = 993
        self.connection: Optional[imaplib.IMAP4_SSL] = None

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
        :return: 邮件列表，每封邮件包含 id、subject、from、from_email、date
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
                
                # 提取发件人邮箱地址
                from_email = ""
                # 尝试从邮件头中获取完整的发件人信息
                raw_from = email_message.get("From", "")
                if "<" in raw_from and ">" in raw_from:
                    from_email = raw_from[raw_from.find("<")+1:raw_from.find(">")]
                elif "@" in raw_from:
                    from_email = raw_from
                
                mail_list.append({
                    "id": email_id.decode(),
                    "subject": subject,
                    "from": from_addr,
                    "from_email": from_email,
                    "date": email_message["Date"]
                })
            
            return mail_list
        except Exception as e:
            print(f"获取邮件列表失败: {str(e)}")
            return [] 