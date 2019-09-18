
# Flask 论坛项目

## 论坛功能简介

- 用户功能：注册、登陆、个人主页、资料修改（用户名、个性签名、头像）。
- 论坛功能：帖子发表、修改、删除、话题板块选择，恢复功能， Markdown 格式支持， 回复/阅读量显示。
- 私信功能： 站内信、邮件通知，评论 @ 邮件通知。

## 论坛配置简介

- 一键脚本快速部署，降低部署难度。
- 使用密码加盐，XSRF token、XSS 防范保证网站安全。
- Nginx 配置反向代理、配置HTTPS 协议增加安全性。
- 使用 MySQL 存储用户数据，使用 Pyalchemy 实现 ORM 同时进行优化。
- 针对频繁读取数据使用 Redis 进行缓存优化，降低路由开销，提高网站特定网页并发能力。
- 使用 Redis 实现服务器端 Session，替代 Flask 内置不安全 Session，并实现进程间数据共享。
- 利用异步任务队列处理站内信、注册邮件发送，保证信息发送成功并立即返回结果，提升用户体验。

# 项目演示

- 一键部署

![一键部署](https://github.com/Auraxc/Flask_web/blob/master/image/一键部署.gif)

- XSRF 防范

![XSRF 防范](https://github.com/Auraxc/Flask_web/blob/master/image/XSRF 防范.gif)

- XSS 防范

![XSS 防范](https://github.com/Auraxc/Flask_web/blob/master/image/XSS 防范.gif)

- 登陆

![登陆](https://github.com/Auraxc/Flask_web/blob/master/image/登陆.gif)

- 密码找回

![密码找回](https://github.com/Auraxc/Flask_web/blob/master/image/密码找回.gif)

- 个人设置及个人中心

![个人设置及个人中心](https://github.com/Auraxc/Flask_web/blob/master/image/个人设置及个人中心.gif)

- 话题发布

![话题发布](https://github.com/Auraxc/Flask_web/blob/master/image/话题发布.gif)

- 后台管理

![后台管理](https://github.com/Auraxc/Flask_web/blob/master/image/后台管理.gif)
