import java.util.Arrays;
import java.util.Random;

public class TestSSS {

	public static void main(String[] args) {
		ThresholdSecretSharing thresholdSecretSharing = new ThresholdSecretSharing();
		//秘密值
		byte[] secret = Hex.convert("a13ff17abef0eec6ac498a0572f6418e6786e79503ce486393f7b9a819af2799");
		//分割份额
		int shares = 50;
		//门限值
		int threshold = 13;
		Random rnd = new Random();
		//生成秘密份额
		long begintime1 = System.nanoTime();
		byte[][] share = thresholdSecretSharing.createShares(secret, shares, threshold, rnd);
		long endtime1 = System.nanoTime();
		long costTime1 = (endtime1 - begintime1)/1000;
		//打印结果
		for (int i = 0; i < share.length; i++) {
			System.out.printf("%2d", share[i][0]);
			System.out.println("---" + Hex.convert(Arrays.copyOfRange(share[i], 1, share[i].length)));
		}
		System.out.println("----------Overheads----------");
		System.out.println("time of generate shares:" + costTime1);
		//重组秘密值
		byte [] share_1 = Hex.convert("01"+"78DC661C06FAA9F74A07E7E466ECE5BE9B71D88B6F9D48D289D02003750DD9A0");
		byte [] share_2 = Hex.convert("02"+"96B9FBC4F45371F60FEB04C38C206980771B5C7C00354D79FF9F9BFE2C6C23E1");
		byte [] share_3 = Hex.convert("03"+"D609BD81565D483945C64270DFF4DA97359FCD07DDFAE1B68A7FD2A6BAE3ED03");
		byte [] share_4 = Hex.convert("04"+"647FBC34C1650F5345CF06DEF86E8715BCE24BE92B5E376B00BD38C86C8DDA87");
		byte [] share_5 = Hex.convert("05"+"51527B89B554B4977BEBDD5DE51AE64E89DC81897CF540BF6E9307F5A94A1C2D");
		byte [] share_6 = Hex.convert("06"+"53B51DE32A550283594839ED8750553A1B21B5A3B2353E4E513835CC34BDB7E4");
		byte [] share_7 = Hex.convert("07"+"CCE7F057CE0CF85A4B3A4EED87F9FF633D4713AC39DF64C863D1704D5B5DDCE4");
		byte [] share_8 = Hex.convert("08"+"278550B0EC550CCA4AAC461D5774DBB0FC63E48B596B47FBC4FA662A2C96B7FD");
		byte [] share_9 = Hex.convert("09"+"824A9349FEF3727F3DF4242EA21F900CA314974342EB15BE14AC13F572B6843F");
		byte [] share_a = Hex.convert("0a"+"E2426F2F5AE7BBE74FF0673AF2214E6EC4605EFD0F2827E2657F69BC1FA811BD");
		byte [] share_b = Hex.convert("0b"+"83137317CD7968C29B721F164B1FAD754940F168ED374A2644C0EB2081B2D10D");
		byte [] share_c = Hex.convert("0c"+"B836392249C55A13AB62BB81617010506131DD891018D1C700F73334A142E306");
		byte [] share_d = Hex.convert("0d"+"7692FF0FA2ACC666A4F11F61E5FDB96B273E9777FBFE2DEE9F4CC50550AD81A7");
		long begintime2 = System.nanoTime();
		byte [] result = thresholdSecretSharing.recoverSecret(share_1, share_2, share_3, share_4, share_5, share_6, share_7, share_8, share_9, share_a, share_b, share_c, share_d);
		long endtime2 = System.nanoTime();
		long costTime2 = (endtime2 - begintime2)/1000;
		System.out.println("time of combine shares:  " + costTime2);
		System.out.println("**---" + Hex.convert(secret));
		System.out.println("++---" + Hex.convert(result));
	}
}
