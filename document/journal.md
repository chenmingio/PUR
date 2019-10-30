# Development Journal

## Requirement Tracking

- [ ] use bootstrap or google CSS framework
- [ ] add logging system
- [ ] data coverage 60%
- [ ] data coverage 80%
- [ ] data coverage 100%
- [ ] pressure test for bottle module
- [ ] check the SQL module robustness
- [x] test if SQL module can share one cursor?
- [ ] build seperate DB connection for another location
- [ ] nginx optimise (support differenct routes and apps)
- [ ] supervisor optimise (auto reload)
- [ ] try ORM and OOP style
- [ ] folder stucture optimisation
- [ ] folder name optimisation
- [ ] do I need thread/quque setting? [Python Exceptions: An Introduction – Real Python](https://realpython.com/python-exceptions/)
- [ ] try - catch cycle?
- [ ] optimise data/number format with ','


## Work Logs

### 2019/10/29

#### test if SQL module can share one cursor?

No. 
* [python - What are the side-effects of reusing a sqlite3 cursor? - Stack Overflow](https://stackoverflow.com/questions/54395773/what-are-the-side-effects-of-reusing-a-sqlite3-cursor)
* [Using a global sqlite cursor across multiple classes? : learnpython](https://www.reddit.com/r/learnpython/comments/94i4k9/using_a_global_sqlite_cursor_across_multiple/)


#### Logging function

[Logging in Python – Real Python](https://realpython.com/python-logging/)

[Logging Cookbook — Python 3.5.7 documentation](https://docs.python.org/3.5/howto/logging-cookbook.html)

[Python Logging Basics - The Ultimate Guide To Logging](https://www.loggly.com/ultimate-guide/python-logging-basics/)

[Logging HOWTO — Python 3.8.0 documentation](https://docs.python.org/3.8/howto/logging.html#logging-basic-tutorial)

[logging.config — Logging configuration — Python 3.7.5 documentation](https://docs.python.org/3.7/library/logging.config.html) logging.conf参数的含义

#### Exception handle

[Python Exceptions: An Introduction – Real Python](https://realpython.com/python-exceptions/)

## Debug Logs

### problem:

- [ ] RE part avg. qty and target price missing for part 178.576-50 and 236.902-60 178.576-15