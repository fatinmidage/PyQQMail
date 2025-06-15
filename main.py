from mail_client import QQMail

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