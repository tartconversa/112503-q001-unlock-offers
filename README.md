# 短剧解锁方案的收入试验与退款保护

短剧解锁权益、随机分派与收入流水。日期按业务日，金额为人民币分。实验分层的计量单位是账户关系表中的主体，src_rev 代表输入更正版本。 观察窗从分派日算起，含分派当日。收入事件用财务入账日，账单退款期从扣款日开始。W1 和 W2 的金额分析单位相同，限量按活动发布的主体权益计。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- trial.csv 的字段为 wave、stratum、starts、ends、watch_days、refund_days、ad_quota、balance_quota。
- identity.csv 的字段为 account、subject、start、stop、src_rev。
- episode_map.csv 的字段为 edition、episode、canonical、coverage、src_rev。
- assignments.csv 的字段为 assignment、wave、stratum、account、offer、at。
- observations.csv 的字段为 observation、assignment、edition、episode、kind、at、entitlement。
- entitlements.csv 的字段为 entitlement、assignment、edition、episode、at、state、parent。
- ledger.csv 的字段为 entry、entitlement、kind、cents、booked_on、adjusts。
- trial_actions.csv 的字段为 action、wave、kind、at、account、source。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
