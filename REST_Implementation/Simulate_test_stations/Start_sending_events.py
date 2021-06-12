import argparse
from Send_to_REST_Server import Rest

# Get command line arguments
parser = argparse.ArgumentParser(description="Configure Input")
parser.add_argument('teststation', type=str, help='All teststations or specific teststation. Ex: All, T1 or T2')
parser.add_argument('product_type', type=str, help='All, PT1 or PT2')
args = parser.parse_args()

# initiate batch_training 
def start_sending_events():
    Rest(args.teststation, args.product_type)

if __name__ == '__main__':
    start_sending_events()