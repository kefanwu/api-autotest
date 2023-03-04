import sys
from gmssl import sm2
from base64 import b64encode, b64decode

# sm2的公私钥
SM2_PRIVATE_KEY = '6240094a022b795bbdfccd737294d0623c3102f7e56b33c0162d596b4a417403'
SM2_PUBLIC_KEY = '045087efca24b3109b8ccf15f33a179d7ee0497beed47be067fd30a04b410cc83b8d543778f3af33c1c94224ff211b367313892a81cff42371dd03bdd2a31dc499'

sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)


# 加密
def encrypt(info):
    encode_info = sm2_crypt.encrypt(info.encode())
    encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
    return encode_info


# 解密
def decrypt(info):
    decode_info = b64decode(info.encode())  # 通过base64解码成二进制bytes
    decode_info = sm2_crypt.decrypt(info).decode(encoding="utf-8")
    return decode_info


if __name__ == "__main__":
    encrypted_contact_info = encrypt('803891Q0TLDY')
    print(encrypted_contact_info)
    # decrypted_contact_info = decrypt(
    #     'QeL44wHoIUjhloToycbLrVqN2pP2G6QiYcm+ONV9ISKBEsO2/RAqF6CXySsQZvnPEg4ccwStqGGwBXgP4D2hCDlGoYw4S5UzB/7UlKGiSxPYirNHqVV3HbyCNwch2vFddyqtvs8ClC3XqfMp')
    # print(decrypted_contact_info)
