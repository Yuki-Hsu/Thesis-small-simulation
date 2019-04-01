import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.SecureRandom;
import java.security.Signature;
import java.security.SignatureException;
import java.security.interfaces.ECPrivateKey;
import java.security.spec.ECGenParameterSpec;
import java.security.PublicKey;

public class ECDSA {

	public static void main(String[] args) {
		// 初始化生成密钥
		long begintime1 = System.nanoTime();
		KeyPair keyPair = setup();
		long endtime1 = System.nanoTime();
		long costTime1 = (endtime1 - begintime1)/1000;
		// 生成签名
		byte[] message = message();
		String algorithm = "SHA256withECDSA";
		long begintime2 = System.nanoTime();
		byte[] signData = signData(algorithm, message, keyPair.getPrivate());
		long endtime2 = System.nanoTime();
		long costTime2 = (endtime2 - begintime2)/1000;
		System.out.println("----------Signature Info----------");
		System.out.println("length of signature: " + signData.length);
		System.out.print("content of signature:");
		for (int i = 0; i < signData.length; i++) {
			System.out.print(Integer.toHexString(signData[i]));
		}
		System.out.println();
		// 验证签名
		long begintime3 = System.nanoTime();
		boolean verify = verifySign(algorithm, message, keyPair.getPublic(), signData);
		long endtime3 = System.nanoTime();
		long costTime3 = (endtime3 - begintime3)/1000;
		System.out.println("----------Verification Results----------");
		System.out.println(verify);
		// 统计时间
		System.out.println("----------Overheads----------");
		System.out.println("Initialization:" + costTime1);
		System.out.println("Sign phase:    " + costTime2);
		System.out.println("Verify phase:  " + costTime3);
	}
	
	public static KeyPair setup() {
		KeyPairGenerator keyPairGenerator = null;
		try {
			keyPairGenerator = KeyPairGenerator.getInstance("EC");
		} catch (NoSuchAlgorithmException e1) {
			e1.printStackTrace();
		}
		// curveName这里取值：secp256k1
		String curveName = "secp256k1";
		ECGenParameterSpec ecGenParameterSpec = new ECGenParameterSpec(curveName);
		try {
			keyPairGenerator.initialize(ecGenParameterSpec, new SecureRandom());
		} catch (InvalidAlgorithmParameterException e) {
			e.printStackTrace();
		}
		KeyPair keyPair = keyPairGenerator.generateKeyPair();
		// 获取公钥
		PublicKey publicKey = keyPair.getPublic();
		// 获取私钥
		PrivateKey privateKey = keyPair.getPrivate();
		System.out.println("----------PublicKey Info----------");
		System.out.println(publicKey);
		System.out.println("----------PrivateKey Info----------");
		System.out.println("decimal:    " + ((ECPrivateKey)privateKey).getS());
		System.out.println("hexadecimal:" + ((ECPrivateKey)privateKey).getS().toString(16));
		return keyPair;
	}
	
	// 生成签名信息
	public static byte[] signData(String algorithm, byte[] data, PrivateKey privateKey) {
        Signature signer = null;
		try {
			signer = Signature.getInstance(algorithm);
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
        try {
			signer.initSign(privateKey);
		} catch (InvalidKeyException e) {
			e.printStackTrace();
		}
        try {
			signer.update(data);
		} catch (SignatureException e) {
			e.printStackTrace();
		}
        try {
			return (signer.sign());
		} catch (SignatureException e) {
			e.printStackTrace();
		}
		return null;
    }

	// 验证签名
    public static boolean verifySign(String algorithm, byte[] data, PublicKey publicKey, byte[] sig) {
        Signature signer = null;
		try {
			signer = Signature.getInstance(algorithm);
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
        try {
			signer.initVerify(publicKey);
		} catch (InvalidKeyException e) {
			e.printStackTrace();
		}
        try {
			signer.update(data);
		} catch (SignatureException e) {
			e.printStackTrace();
		}
        try {
			return (signer.verify(sig));
		} catch (SignatureException e) {
			e.printStackTrace();
		}
		return false;
    }

    public static byte[] message() {
        // 需要签名的数据
        byte[] data = new byte[100];
        for (int i=0; i<data.length; i++)
            data[i] = 0xb;
        return data;
    }
}
