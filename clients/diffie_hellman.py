import binascii


# inspired by https://github.com/amiralis/pyDH/blob/master/pyDH/pyDH.py

def gen_public_key(private_key: bytes):
    # RFC 3526 - More Modular Exponential (MODP) Diffie-Hellman groups for
    # Internet Key Exchange (IKE) https://tools.ietf.org/html/rfc3526

    # using 2048-bit MODP Group (group 14)
    # compliant according to the ANSSI: https://www.ssi.gouv.fr/uploads/2012/09/NT_IPsec_EN.pdf page 16/R16

    prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    generator = 2

    # converting cli_secret into int

    a = int(
        binascii.hexlify(private_key),
        16
    )

    # computing g^a mod p
    public_key = pow(generator, a, prime)

    return public_key
