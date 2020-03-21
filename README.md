# Thesis-small-simulation

🔑🔑🔑ECDSA &amp;&amp; Shamir's Secret Sharing Scheme

## References

http://point-at-infinity.org/ssss/

https://gitbook.cn/books/5c7b827effa76e7af9186329/index.html

https://www.jianshu.com/p/e6ac2c75e692

## Descriptions

`WCRT+TECDSA.py` using python 3.8.2 to simulate the whole procedures of secret sharing based on WCRT combined threshold ECDSA based on Shamir secret sharing. The default threshold is `t = 6`, the participating users are `\overline{n} = 5` with weights are `[2, 3, 1, 1, 1]`.

### Usage

- `pip install bitcoin`
- Modify the source code and then `python WCRT+TECDSA.py > 1.txt` to get appropriate coprime integers sequence
- Modify the source code to apply appropriate coprime integers sequence and then `python WCRT+TECDSA.py`

### Useful Knowledge

https://www.runoob.com/python/python-func-range.html (pay attention to the difference between python 2.X and python 3.X)

[python实现模逆运算](https://blog.csdn.net/CosmopolitanMe/article/details/78948011)

https://github.com/vbuterin/pybitcointools

https://python3-cookbook.readthedocs.io/zh_CN/latest/c03/p08_calculating_with_fractions.html

https://docs.python.org/zh-cn/3/library/fractions.html

https://github.com/cxz111111/PYchain
