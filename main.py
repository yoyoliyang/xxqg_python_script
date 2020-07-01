#!/usr/bin/python3
import uiautomator2 as u2
import time
import random
import os
import notice

# android phone: 执行/data/local/tmp/atx-agent server -d 来进行启动agent操作，可以安装“脚本”app来方便执行。
d = u2.connect_wifi("192.168.1.37")
#d = u2.connect("192.168.1.37")

# device.app_start("cn.xuexi.android")  # 启动学习强国package

xpath_dic = {
    '我的': 'cn.xuexi.android:id/comm_head_xuexi_mine',
    '我的积分': '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]',
    '阅读文章': '//android.widget.ListView/android.view.View[2]/android.view.View[4]',
    '视听学习': '//android.widget.ListView/android.view.View[3]/android.view.View[4]',
    # 要闻(文章)频道入口按钮
    '要闻': '//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.View[1]/android.widget.LinearLayout[2]',
    # 视频学习频道入口按钮
    '电视台': '//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]',
    '联播频道': '//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.View[1]/android.widget.LinearLayout[3]',
    'back_button': '//*[@resource-id="cn.xuexi.android:id/TOP_LAYER_VIEW_ID"]/android.widget.ImageView[1]',
    'video_back_button': '//*[@resource-id="cn.xuexi.android:id/EXTRA_INFO_LAYER_VIEW_ID"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[3]/android.widget.ImageView[1]'
}

old_list = []  # 读过的列表
news_list = []  # 定义一个空列表保存news标题用来检测是否重复
video_news_list = []


def save_list():  # 保存读过的标题
    print(news_list)
    with open('list.log', 'a') as f:
        for i in news_list:
            f.write(i+'\n')


def load_list():  # 加载读过的文章到列表
    if os.path.exists('list.log'):
        with open('list.log') as f:
            for i in f.readlines():
                old_list.append(i.strip())
    else:
        return


def learning(isVideo=None):
    news_xpath_outside = d.xpath(
        '//android.widget.ListView/android.widget.FrameLayout').all()
    # 找到news所在的外部框架,用于click
    news_xpath_inside = d.xpath(
        "@cn.xuexi.android:id/general_card_title_id").all()
    # 找到news的标题内容,用于后期判断是否已经阅读
    for x, y in zip(news_xpath_outside, news_xpath_inside):
        if y.text in old_list:
            print('跳过读过的文章')
            pass
        else:
            news_list.append(y.text)
            print('正在阅读：{}'.format(y.text))
            x.click()
            # 下面是处理阅读页面的事件
            if isVideo is True:
                video_wait_time = random.randint(120, 180)
                time.sleep(video_wait_time)  # 此处定义视频学习时长
                video_news_list.append(y.text)  # 视频列表递增
                print('当前学了{}篇视频'.format(len(video_news_list)))
                d.xpath(xpath_dic['video_back_button']).click()
                time.sleep(2)
            else:
                news_wait_time = random.randint(50, 60)  # 新闻时长,并卷动屏幕
                while True:
                    news_wait_time = news_wait_time - 1
                    if news_wait_time <= 0:
                        break
                    d.swipe_ext('up', scale=0.1)
                    time.sleep(1)
                d.xpath(xpath_dic['back_button']).click()
                print('当前学了{}篇新闻'.format(len(news_list)))
                time.sleep(2)
            if len(news_list) == 6:
                print('已经学完{}篇新闻'.format(len(news_list)))
                break
            if len(video_news_list) == 6:
                print('已经学完{}篇视频'.format(len(video_news_list)))
                break


def score():
    d(resourceId="cn.xuexi.android:id/home_bottom_tab_button_work").click()
    scores = d(resourceId="cn.xuexi.android:id/comm_head_xuexi_score").get_text()
    return int(scores)


load_list()
print(old_list)
# 点击主页按钮返回到主页
d(resourceId="cn.xuexi.android:id/home_bottom_tab_button_work").click()
# 获取学习前总积分
old_score = score() - 1
print(f'当前学习总积分： {old_score}')  # 排除登录获取的1分
print('开始学习新闻')
d.xpath(xpath_dic['要闻']).click()  # 进入栏目入口
time.sleep(3)
learning()
while len(news_list) < 6:
    d.swipe_ext('up', scale=0.4)  # 上划80%屏幕
    time.sleep(3)
    print('没有学够，继续学习')
    learning()

# 确保返回主页
d(resourceId="cn.xuexi.android:id/home_bottom_tab_button_work").click()

print('开始学习视频')
d.xpath(xpath_dic['电视台']).click()  # 进入栏目入口
time.sleep(3)
d.xpath(xpath_dic['联播频道']).click()
time.sleep(3)
learning(isVideo=True)
while len(video_news_list) < 6:
    d.swipe_ext('up', scale=0.4)  # 上划80%屏幕
    time.sleep(3)
    print('没有学够，继续学习')
    learning(isVideo=True)

save_list()
print('学习完毕')
current_score = score() - old_score
print(f'今日学习积分： {current_score}')
notice.send(f'强国学习完毕，今日学习积分：{current_score}')
