import requests
import pandas as pd
import matplotlib
# 使用 Agg 后端，这样在无显示器的云端环境也能正常保存图片
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 注意：这里删除了 proxies，因为 GitHub 服务器直接连外网

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 设置中文字体（如果云端报错找不到字体，图表上的中文可能会变方块，但不影响数据）
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

def spy_jobs():
    print("\\n[1/2] 正在潜入全球远程工作节点 (RemoteOK)...")
    url = "https://remoteok.com/api"
    try:
        # 删除了 proxies=proxies
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data[1:]: 
                company = job.get('company', '未知')
                position = job.get('position', '未知')
                salary_min = job.get('salary_min', 0)
                salary_max = job.get('salary_max', 0)
                
                if salary_min > 0:
                    jobs.append({
                        '公司': company,
                        '职位': position,
                        '最低年薪($)': salary_min,
                        '最高年薪($)': salary_max
                    })
            
            df_jobs = pd.DataFrame(jobs)
            if not df_jobs.empty:
                df_jobs['平均年薪($)'] = (df_jobs['最低年薪($)'] + df_jobs['最高年薪($)']) / 2
                df_jobs = df_jobs.sort_values(by='平均年薪($)', ascending=False)
                df_jobs.to_excel('全球高薪技术岗位.xlsx', index=False)
                print(f" -> 截获 {len(df_jobs)} 个高薪岗位，已存入 Excel")
            else:
                print(" -> 暂未截获带有明确薪资的岗位。")
        else:
            print(" -> 岗位侦察失败，状态码:", response.status_code)
    except Exception as e:
        print(" -> 岗位侦察断网:", e)

def spy_news():
    print("\\n[2/2] 正在潜入全球极客情报中枢 (Hacker News)...")
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
                    news_data.append({'新闻标题': title, '热度': score})
            
            df_news = pd.DataFrame(news_data)
            df_news.to_excel('全球极客热搜.xlsx', index=False)
            print(f" -> 截获 {len(df_news)} 条全球核心热搜，已存入 Excel")
            
            plt.figure(figsize=(10, 6))
            df_news = df_news.iloc[::-1] 
            df_news['短标题'] = df_news['新闻标题'].apply(lambda x: x[:40] + '...' if len(x) > 40 else x)
            
            plt.barh(df_news['短标题'], df_news['热度'], color='skyblue')
            plt.title('Global Tech Hot Topics', fontsize=16)
            plt.xlabel('Score', fontsize=12)
            plt.tight_layout()
            
            # 【注意这里】云端不弹窗，直接保存为图片
            plt.savefig('全球热搜图.png', dpi=150)
            print(" -> 图表已保存为 全球热搜图.png")
            
        else:
            print(" -> 新闻侦察失败，状态码:", response.status_code)
    except Exception as e:
        print(" -> 新闻侦察断网:", e)

print("====== 宏观双线侦察行动开始 ======")
spy_jobs()
spy_news()
print("\\n====== 侦察行动结束 ======")