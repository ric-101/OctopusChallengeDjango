# OctopusChallengeDjango

## Language and word selection
While hidden from the user, the class tools.LanguageParser, already supports the possiblity of selecting only certain languages or types of words (given that the proper language file is present in the resources)

## Key Security
At the moment, both the salt of the hash function and the symettric-encryption key are stored as plain text in settings.py. This is resonably secure as long as the souce codes are kept private and the server's access properly managed.
To increase security it is possible to take further measures, such as storing the key on the server (i.e. on a file) so that it does not travel with the sources. Even further security could be achieved having one centralized server, with very restricted access, which provides encryption and decryption as a service, only to allowed clients which can access it securely (not abblicable to hashing if the primary key, excepet at a very high performance cost).
If possbile, chaning the keys often and adding salts even to the words, helps against statistical attacks.



