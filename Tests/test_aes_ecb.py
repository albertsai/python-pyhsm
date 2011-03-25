import sys
import unittest
import pyhsm

import test_common

class TestOtpValidate(test_common.YHSM_TestCase):

    def setUp(self):
        # Enabled flags 00007000 = YHSM_ECB_BLOCK_ENCRYPT,YHSM_ECB_BLOCK_DECRYPT,YHSM_ECB_BLOCK_DECRYPT_CMP
        self.kh_encrypt = 0x1001
        self.kh_decrypt = 0x1001
        self.kh_compare = 0x1001

        self.hsm = pyhsm.base.YHSM(device = "/dev/ttyACM0", debug = False)

        # Check that this is a device we know how to talk to
        assert(self.hsm.info().protocolVersion == 1)

    def test_encrypt_decrypt(self):
        """ Test to AES ECB decrypt something encrypted. """
        plaintext = 'Fjaellen 2011'.ljust(pyhsm.defines.YHSM_BLOCK_SIZE)	# pad for compare after decrypt

        ciphertext = self.hsm.aes_ecb_encrypt(self.kh_encrypt, plaintext)

        self.assertNotEqual(plaintext, ciphertext)

        decrypted = self.hsm.aes_ecb_decrypt(self.kh_decrypt, ciphertext)

        self.assertEqual(plaintext, decrypted)

    def test_compare(self):
        """ Test to AES ECB decrypt and then compare something. """
        plaintext = 'Maverick'.ljust(pyhsm.defines.YHSM_BLOCK_SIZE)

        ciphertext = self.hsm.aes_ecb_encrypt(self.kh_encrypt, plaintext)

        self.assertTrue(self.hsm.aes_ecb_compare(self.kh_compare, ciphertext, plaintext))
        self.assertFalse(self.hsm.aes_ecb_compare(self.kh_compare, ciphertext, 'x' + plaintext))