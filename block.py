

from hashlib import sha256
import json
import time

class Block:

    """
    Les transactions sont regroupées en blocs. Un bloc peut contenir une ou plusieurs transactions.
    Les blocs contenant les transactions sont générés fréquemment et ajoutés à la blockchain. 
    Parce qu'il peut y avoir plusieurs blocs, chaque bloc doit avoir un ID unique:
    """

    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for the `Block` class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions.
        :param timestamp: Time of generation of the block.
        :param previous_hash: Hash of the previous block in the chain which this block is part of.
        :param nonce: Value of difficulty
        """
        self.index = index 
        self.transactions = transactions 
        self.timestamp = timestamp
        self.previous_hash = previous_hash # Adding the previous hash field / file remarque.txt 2**-
        self.nonce = 0

    """
    Il existe différentes fonctions de hachage populaires. Ici nous utiliserons le SHA-256 le même que Bitcoin.
    Nous allons stocker le hachage du bloc dans un champ à l'intérieur de notre Block objet, 
    et il agira comme une empreinte digitale numérique (ou signature) des données qu'il contient:
    """

    def compute_hash(self):
        """
        Returns the hash of the block instance by first converting it
        into JSON string.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
        # file remarque.txt 1**-
    


class Blockchain:
    """ 
    Structure de base de notre blockchain
    """

    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        """
        Constructor for the `Blockchain` class.
        """
        self.unconfirmed_transactions = [] # data yet to get into blockchain
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        A quick pythonic way to retrieve the most recent block in the chain. Note that
        the chain will always consist of at least one block (i.e., genesis block)
        """
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
        # file remarque.txt 3**-
    

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())


    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
        in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False
        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
        # file remarque.txt 4**-

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
        # file remarque.txt 5**-

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out proof of work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)
        
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
        # file remarque.txt 6**- 
