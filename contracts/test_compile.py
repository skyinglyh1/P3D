import binascii
from boa.compiler import Compiler

def hexlify_avm(blob):
    return binascii.hexlify(blob).decode('ascii')


def read_avm(filename):
    with open(filename, 'rb') as f:
        return hexlify_avm(f.read())
def save_avm(filename, a):
    with open(filename,'w') as f:
        f.write(a)


if __name__ == '__main__':
    # # path=os.path.join(os.getcwd(),'contracts','test_contract.py')
    Compiler.load_and_save("./contracts/test_contract.py")
    # Compiler.load_and_save("AddTest.py", './contracts/out_AddTest.txt')

    # save_avm(avm_file_path, read_avm('contracts/test_contract.avm'))


