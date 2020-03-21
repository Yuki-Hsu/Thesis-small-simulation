import math
import fractions
import bitcoin

# 判断是否为素数
def isPrime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num) + 1)):
        if num % i == 0:
            return False
    return True

# 筛选一个区间范围内的所有素数并将素数结果存到一个列表中
def listPrimes(begin, end):
    COLUMN = 10
    count = 0
    list_primes = []
    for num in range(begin, end):
        if isPrime(num):
            print("%d\t" % num, end = "")
            count += 1
            list_primes.append(num)
            if count % COLUMN == 0:
                print()
    print()
    return list_primes

# 给定门限值和素数列表集合，筛选出满足中国剩余定理秘密共享方案中的互素正整数序列，并给出秘密值的取值范围
def crtSecretSharing(list_primes, t):
    count = len(list_primes)
    for i in range(count - t):
        # 计算 最小的 t 个数乘积
        t_interval_left = i
        t_interval_right = i + t
        t_product = 1
        for j in range(t_interval_left, t_interval_right):
            t_product *= list_primes[j]
        # 向后依此寻找满足条件 t - 1 个数乘积小于签名 t 个数乘积，并向后扩张该序列
        t_1_interval_left = i + 2
        t_1_interval_right = t_1_interval_left + t -1
        while t_1_interval_right <= count:
            t_1_product = 1
            for j in range(t_1_interval_left, t_1_interval_right):
                t_1_product *= list_primes[j]
            if t_1_product < t_product:
                print("%d\t< secret < %d\t, rate = %.5f\t" % (t_1_product, t_product, t_product/t_1_product), end="")
                print(list_primes[t_interval_left: t_1_interval_right])
                t_1_interval_left += 1
                t_1_interval_right = t_1_interval_left + t -1
            else:
                break

# 求最大公约数
def gcd(a, b):
    while a!=0:
        a, b = b % a, a
    return b

# 使用扩展欧几里得算法求 a * b = 1 mod m
def findModReverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

# 计算二次多项式的结果 f(x) = a_0 + a_1*x + a_2*x*x
def f_x(a_0, a_1, a_2, x):
    return a_0 + a_1*x + a_2*x*x

# 拉格朗日插值恢复秘密值
def lagrange(list_shares):
    secret = 0
    for i in range(len(list_shares)):
        l_i_0 = 1
        # 计算 x = 0 时的拉格朗日插值系数
        for m in range(len(list_shares)):
            if m != i:
                l_i_0 *= fractions.Fraction((m + 1), ((m + 1) - (i + 1)))
                """
                这句代码存在精度损失的问题，已弃用
                # l_i_0 *= (m + 1) / ((m + 1) - (i + 1))
                """
        secret += list_shares[i] * l_i_0
    return secret

# Simple Reciprocal Protocol 协议分发秘密值逆的份额，为了简单省去了其中的 JZSS
def simpleRecPro(list_shares, mod_q, degree = 2):
    if degree == 2:
        """
        5 个玩家分别选择次数为 (5 - 1) / 2 的随机多项式，并让自由项系数为随机数 e_i，运行JRSS，玩家身份索引为 i
        玩家 P1: f(x) = 4 + 3*x + 4*x*x
        玩家 P2: f(x) = 12 + 5*x + 7*x*x
        玩家 P3: f(x) = 9 + 2*x + 4*x*x
        玩家 P4: f(x) = 23 + 7*x + 2*x*x
        玩家 P5: f(x) = 15 + 3*x + 5*x*x
        """
        # 联合共享新的秘密值 e 的份额
        p1_to_others = []
        for i in range(1, 6):
            p1_to_others.append(f_x(4, 3, 4, i))
        p2_to_others = []
        for i in range(1, 6):
            p2_to_others.append(f_x(12, 5, 7, i))
        p3_to_others = []
        for i in range(1, 6):
            p3_to_others.append(f_x(9, 2, 4, i))
        p4_to_others = []
        for i in range(1, 6):
            p4_to_others.append(f_x(23, 7, 2, i))
        p5_to_others = []
        for i in range(1, 6):
            p5_to_others.append(f_x(15, 3, 5, i))
        jrss_e_shares = []
        for i in range(0, 5):
            jrss_e_shares.append(p1_to_others[i] + p2_to_others[i] + p3_to_others[i] + p4_to_others[i] + p5_to_others[i])
        print(jrss_e_shares)
        print("combined_e_i:%d" % (4 + 12 + 9 + 23 + 15))
        print("recover_e_i: %d" % lagrange(jrss_e_shares))
        # Locally compute u_i = list_shares[i] * e_i
        jrss_u_shares = []
        # 计算 u = xe 的份额 u_i，然后恢复出 u
        for i in range(len(list_shares)):
            jrss_u_shares.append(list_shares[i] * jrss_e_shares[i])
        print(jrss_u_shares)
        u = lagrange(jrss_u_shares)
        print("recover_u: %d" % u)
        # 计算 u 的逆
        u_reverse = findModReverse(u, mod_q)
        print("u_reverse: %d" % u_reverse)
        list_shares_reverse = []
        # 计算 x 的逆的份额
        for i in range(len(list_shares)):
            list_shares_reverse.append(jrss_e_shares[i] * u_reverse % mod_q)
        return list_shares_reverse



def main():
    # Setup
    """
    # crtSecretSharing(listPrimes(3000000000000, 3000000010000), 6)
    # crtSecretSharing(listPrimes(10000, 20000), 6)
    由 crtSecretSharing 选取如下序列
    105987830196477595229 < secret < 1022186603775641127185083
    rate = 9644.37711
    [10007, 10009, 10037, 10039, 10061, 10067, 10069, 10079, 10091, 10093, 10099, 10103, 10111, 10133, 10139]
    """
    d = 105987830196477595231  # 随机选择的私钥
    q = bitcoin.N  # 比特币椭圆曲线上点群的阶数
    sequence = [10007, 10009, 10037, 10039, 10061, 10067, 10069, 10079, 10091, 10093, 10099, 10103, 10111, 10133, 10139]
    """
    根据上述正整数序列，假设玩家权重依此为
    [2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    权重为 2，则 10061 * 10067 < p < 10099 * 10103
    权重为 3，则 10039 * 10061 * 10067 < p < 10099 * 10103 * 10111
    # listPrimes(10061 * 10067, 10099 * 10103)
    # listPrimes(10039 * 10061 * 10067, 10039 * 10061 * 10067 + 1000)
    由 listPrimes 更新序列为如下
    """
    weighted_sequence = [101284093, 1016790949397, 10037, 10039, 10061, 10067, 10069, 10079, 10091, 10093, 10099, 10103, 10111, 10133, 10139]
    weighted_shares = []
    for i in weighted_sequence:
        weighted_shares.append(d % i)
    print("weighted_shares:", end = "")
    print(weighted_shares)
    print("lambda:%d" % int(1022186603775641127185083/d))

    # Signature Generation --- Calculating temporary shares
    """
    假设权重值为 2，3，1，1，1 的 5 个玩家参与签名，weighted_sequence[0:5]
    """
    N = weighted_sequence[0] * weighted_sequence[1] * weighted_sequence[2] * weighted_sequence[3] * weighted_sequence[4]
    y_i = []
    d_i = []
    # 使用 N / p_i^j 计算会损失精度，所以将 N / p_i^j 换成如下的连续相乘
    y_i.append(findModReverse(weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[4], weighted_sequence[0]))
    y_i.append(findModReverse(weighted_sequence[0]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[4], weighted_sequence[1]))
    y_i.append(findModReverse(weighted_sequence[1]*weighted_sequence[0]*weighted_sequence[3]*weighted_sequence[4], weighted_sequence[2]))
    y_i.append(findModReverse(weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[0]*weighted_sequence[4], weighted_sequence[3]))
    y_i.append(findModReverse(weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[0], weighted_sequence[4]))
    d_i.append((weighted_shares[0] * weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[4] * y_i[0]) % N)
    d_i.append((weighted_shares[1] * weighted_sequence[0]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[4] * y_i[1]) % N)
    d_i.append((weighted_shares[2] * weighted_sequence[1]*weighted_sequence[0]*weighted_sequence[3]*weighted_sequence[4] * y_i[2]) % N)
    d_i.append((weighted_shares[3] * weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[0]*weighted_sequence[4] * y_i[3]) % N)
    d_i.append((weighted_shares[4] * weighted_sequence[1]*weighted_sequence[2]*weighted_sequence[3]*weighted_sequence[0] * y_i[4]) % N)
    print("y_i:", end = "")
    print(y_i)
    print("d_i:", end = "")
    print(d_i)
    recover_secret = 0
    for i in d_i:
        recover_secret += i
        recover_secret %= N
    print("recover_secret:%d" % recover_secret)

    # Signature Generation --- Calculating temporary shares --- First run JRSS
    """
    5 个玩家分别选择次数为 (5 - 1) / 2 的随机多项式，并让自由项系数为 d_i[i]，运行JRSS，玩家身份索引为 i
    玩家 P1: f(x) = d_i[0] + 3*x + 4*x*x
    玩家 P2: f(x) = d_i[1] + 5*x + 7*x*x
    玩家 P3: f(x) = d_i[2] + 2*x + 4*x*x
    玩家 P4: f(x) = d_i[3] + 7*x + 2*x*x
    玩家 P5: f(x) = d_i[4] + 3*x + 5*x*x
    """
    p1_to_others = []
    for i in range(1, 6):
        p1_to_others.append(f_x(d_i[0], 3, 4, i))
    p2_to_others = []
    for i in range(1, 6):
        p2_to_others.append(f_x(d_i[1], 5, 7, i))
    p3_to_others = []
    for i in range(1, 6):
        p3_to_others.append(f_x(d_i[2], 2, 4, i))
    p4_to_others = []
    for i in range(1, 6):
        p4_to_others.append(f_x(d_i[3], 7, 2, i))
    p5_to_others = []
    for i in range(1, 6):
        p5_to_others.append(f_x(d_i[4], 3, 5, i))
    jrss_1_d_shares = []
    for i in range(0, 5):
        jrss_1_d_shares.append(p1_to_others[i] + p2_to_others[i] + p3_to_others[i] + p4_to_others[i] + p5_to_others[i])
    print(jrss_1_d_shares)
    print("combined_d_i:%d" % (d_i[0]+d_i[1]+d_i[2]+d_i[3]+d_i[4]))
    print("recover_d_i: %d" % lagrange(jrss_1_d_shares))

    # Signature Generation --- Calculating temporary shares --- Second run JRSS
    """
    5 个玩家分别选择次数为 (5 - 1) / 2 的随机多项式，并让自由项系数 v_i <= lambda / 5 = 9644 /5 = 1928.8，运行JRSS，玩家身份索引为 i
    玩家 P1: f(x) = 5 + 3*x + 4*x*x
    玩家 P2: f(x) = 9 + 5*x + 7*x*x
    玩家 P3: f(x) = 10 + 2*x + 4*x*x
    玩家 P4: f(x) = 14 + 7*x + 2*x*x
    玩家 P5: f(x) = 23 + 3*x + 5*x*x
    """
    p1_to_others = []
    for i in range(1, 6):
        p1_to_others.append(f_x(5, 3, 4, i))
    p2_to_others = []
    for i in range(1, 6):
        p2_to_others.append(f_x(9, 5, 7, i))
    p3_to_others = []
    for i in range(1, 6):
        p3_to_others.append(f_x(10, 2, 4, i))
    p4_to_others = []
    for i in range(1, 6):
        p4_to_others.append(f_x(14, 7, 2, i))
    p5_to_others = []
    for i in range(1, 6):
        p5_to_others.append(f_x(23, 3, 5, i))
    jrss_2_v_shares = []
    for i in range(0, 5):
        jrss_2_v_shares.append(p1_to_others[i] + p2_to_others[i] + p3_to_others[i] + p4_to_others[i] + p5_to_others[i])
    print(jrss_2_v_shares)
    print("combined_v_i:%d" % (5 + 9 + 10 + 14 + 23))
    print("recover_v_i: %d" % lagrange(jrss_2_v_shares))

    # Signature Generation --- Calculating temporary shares --- Locally compute v_i*d_i and recover v*d
    jrss_vd_shares = []
    for i in range(0, 5):
        jrss_vd_shares.append(jrss_1_d_shares[i] * jrss_2_v_shares[i])
    print(jrss_vd_shares)
    print("combined_vd:%d" % ((d_i[0]+d_i[1]+d_i[2]+d_i[3]+d_i[4])*(5+9+10+14+23)))
    print("recover_vd: %d" % lagrange(jrss_vd_shares))
    vd = lagrange(jrss_vd_shares) % N
    print("vd mod N: %d" % vd)

    # Signature Generation --- Calculating temporary shares --- Simple Reciprocal Protocol get shares of v^-1 without revealing v and v^-1
    srp_v_reverse_shares = simpleRecPro(jrss_2_v_shares, q)
    print(srp_v_reverse_shares)

    # Signature Generation --- Calculating temporary shares --- Get temporary shares \alpha_i = v_i^-1 * vd mod q of private key d
    alpha_shares = []
    for i in range(0, 5):
        alpha_shares.append(srp_v_reverse_shares[i] * vd % q)
    print("alpha_shares:", end = "")
    print(alpha_shares)
    print("recover_secret:%d" % (lagrange(alpha_shares) % q))

    # Signature Generation --- Calculating the ﬁrst part of signature
    """
    5 个玩家分别选择次数为 (5 - 1) / 2 的随机多项式，并让自由项系数 1 < k_i < q，运行JRSS，玩家身份索引为 i
    玩家 P2: f(x) = 24 + 5*x + 7*x*x mod q
    玩家 P1: f(x) = 89 + 3*x + 4*x*x mod q
    玩家 P3: f(x) = 10 + 2*x + 4*x*x mod q
    玩家 P4: f(x) = 45 + 7*x + 2*x*x mod q
    玩家 P5: f(x) = 23 + 3*x + 5*x*x mod q
    """
    p1_to_others = []
    for i in range(1, 6):
        p1_to_others.append(f_x(24, 3, 4, i))
    p2_to_others = []
    for i in range(1, 6):
        p2_to_others.append(f_x(89, 5, 7, i))
    p3_to_others = []
    for i in range(1, 6):
        p3_to_others.append(f_x(10, 2, 4, i))
    p4_to_others = []
    for i in range(1, 6):
        p4_to_others.append(f_x(45, 7, 2, i))
    p5_to_others = []
    for i in range(1, 6):
        p5_to_others.append(f_x(23, 3, 5, i))
    jrss_k_shares = []
    for i in range(0, 5):
        jrss_k_shares.append(p1_to_others[i] + p2_to_others[i] + p3_to_others[i] + p4_to_others[i] + p5_to_others[i])
    print(jrss_k_shares)
    print("combined_k_i:%d" % (24 + 89 + 10 + 45 + 23))
    print("recover_k_i: %d" % lagrange(jrss_k_shares))
    V_shares = []
    for i in range(len(jrss_k_shares)):
        l_i_0 = 1
        for m in range(len(jrss_k_shares)):
            if m != i:
                l_i_0 *= fractions.Fraction((m + 1), ((m + 1) - (i + 1)))
        V_shares.append(jrss_k_shares[i] * l_i_0)
    print(V_shares)
    """
    将 V_shares 中的 l_i(0) * k_i 转换成比特币私钥，并利用 bitcoin 包计算点乘运算
    为了使用 bitcoin.multiply(pub, priv) 方法，需要将整数 l_i(0) * k_i 转换为长度为 64 的十六进制字符串，不足的需补零。
    或者不转换，直接当作十进制整数赋值给形参 priv
    """
    V_shares_temp = []
    for i in range(len(V_shares)):
        V_shares_temp.append(V_shares[i].numerator % q)
    print(V_shares_temp)
    V_point_shares = []
    for i in V_shares_temp:
        V_point_shares.append(bitcoin.multiply(bitcoin.G, i))
    print(V_point_shares)
    V_point_k_G = V_point_shares[0]
    i = 1
    while i < len(V_point_shares):
        V_point_k_G = bitcoin.add_pubkeys(V_point_k_G, V_point_shares[i])
        i += 1
    print("V_point_k_G:", end = "")
    print(V_point_k_G)
    r = V_point_k_G[0] % q  # 签名对中的 r
    print("r:%d" % r)

    # Signature Generation --- Calculating the second part of signature
    srp_k_reverse_shares = simpleRecPro(jrss_k_shares, q)
    print("srp_k_reverse_shares:", end = "")
    print(srp_k_reverse_shares)
    print("recover_k_reverse:%d" % lagrange(srp_k_reverse_shares))
    """
    计算部分签名 s_i = k_i^-1 * hash + r * alpha_i * k_i^-1 mod q
    """
    message_hash = 123456789  # 待签名消息的哈希
    s_shares = []
    for i in range(len(srp_k_reverse_shares)):
        s_shares.append((srp_k_reverse_shares[i] * message_hash + r * alpha_shares[i] * srp_k_reverse_shares[i]) % q)
    s = lagrange(s_shares) % q  # 签名对中的 s
    print("s:%d" % s)

    # Signature Verification
    Q = bitcoin.multiply(bitcoin.G, d)  # 私钥对应的公钥
    w = findModReverse(s, q)
    u1 = message_hash * w % q
    u2 = r * w % q
    final_point = bitcoin.add_pubkeys(bitcoin.multiply(bitcoin.G, u1), bitcoin.multiply(Q, u2))
    print(final_point[0] % q)


if __name__ == "__main__":
    main()