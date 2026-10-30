import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import yagmail
import translators as ts

# 解决云端 Linux 系统没有中文字体的问题
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def translate_text(text):
    if not text or text == '未知':
        return text
    try:
        # 使用必应翻译通道，对 GitHub 服务器更友好
        translated = ts.translate_text(text, translator='bing', from_language='en', to_language='zh')
        return translated
    except Exception as e:
        # 失败则保留原文
        return text

def spy_jobs():
    print("\\n[1/3] 正在潜入全球远程工作节点 (RemoteOK)...")
    url = "https://remoteok.com/api"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data[1:]:
                company = job.get('company', '未知')
                position = job.get('position', '未知')
                salary_min = job.get('salary_min', 0)
                salary_max = job.get('salary_max', 0)
                
                if salary_min > 30000:
                    translated_position = translate_text(position)
                    jobs.append({
                        '公司': company,
                        '职位(中文)': translated_position,
                        '职位(英文原版)': position,
                        '最低年薪($)': salary_min,
                        '最高年薪($)': salary_max
                    })
            
            df_jobs = pd.DataFrame(jobs)
            if not df_jobs.empty:
                df_jobs['平均年薪($)'] = (df_jobs['最低年薪($)'] + df_jobs['最高年薪($)']) / 2
                df_jobs = df_jobs.sort_values(by='平均年薪($)', ascending=False)
                df_jobs.to_excel('全球高薪技术岗位.xlsx', index=False)
                print(f" -> 截获 {len(df_jobs)} 个岗位，已翻译并存入 Excel")
            else:
                print(" -> 暂未截获岗位。")
        else:
            print(" -> 侦察失败:", response.status_code)
    except Exception as e:
        print(" -> 岗位侦察断网:", e)

def spy_news():
    print("\\n[2/3] 正在潜入全球极客情报中枢 (Hacker News)...")
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(top_stories_url, timeout=15)
        if response.status_code == 200:
            story_ids = response.json()[:15]
            news_data = []
            for s_id in story_ids:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                item_res = requests.get(item_url, timeout=10)
                if item_res.status_code == 200:
                    item = item_res.json()
                    title = item.get('title', '未知标题')
                    score = item.get('score', 0)
                    
                    translated_title = translate_text(title)
                    news_data.append({
                        '新闻标题(中文)': translated_title,
                        '新闻标题(英文原版)': title,
                        '热度': score
                    })
            
            df_news = pd.DataFrame(news_data)
            df_news.to_excel('全球极客热搜.xlsx', index=False)
            print(f" -> 截获 {len(df_news)} 条热搜，已翻译并存入 Excel")
            
            plt.figure(figsize=(10, 6))
            df_news = df_news.iloc[::-1] 
            df_news['短标题'] = df_news['新闻标题(中文)'].apply(lambda x: x[:15] + '...' if len(x) > 15 else x)
            plt.barh(df_news['短标题'], df_news['热度'], color='skyblue')
            plt.title('全球极客今日关注热度榜', fontsize=16)
            plt.xlabel('热度 (Score)', fontsize=12)
            plt.tight_layout()
            plt.savefig('全球热搜图.png', dpi=150)
            print(" -> 中文图表已保存")
            plt.close()
        else:
            print(" -> 新闻侦察失败:", response.status_code)
    except Exception as e:
        print(" -> 新闻侦察断网:", e)

def send_email():
    print("\\n[3/3] 正在打包情报，发送至指定邮箱...")
    mail_user = os.environ.get('MAIL_USER')
    mail_pass = os.environ.get('MAIL_PASS')
    mail_to = os.environ.get('MAIL_TO')

    if not mail_user or not mail_pass or not mail_to:
        print(" -> 发送失败: 邮箱配置为空。")
        return

    try:
        yag = yagmail.SMTP(user=mail_user, password=mail_pass, host='smtp.163.com')
        subject = "【宏观智能】今日数据情报已送达（中文版）"
        contents = "主公，今日的全球高薪岗位与新闻热搜（已翻译）请查阅附件。"
        attachments = ['全球高薪技术岗位.xlsx', '全球极客热搜.xlsx', '全球热搜图.png']
        yag.send(to=mail_to, subject=subject, contents=contents, attachments=attachments)
        print(" -> 邮件发送成功！")
    except Exception as e:
        print(f" -> 邮件发送失败: {e}")

if __name__ == "__main__":
    print("====== 宏观双线侦察行动开始 ======")
    spy_jobs()
    spy_news()
    send_email()
    print("====== 侦察行动结束 ======")
