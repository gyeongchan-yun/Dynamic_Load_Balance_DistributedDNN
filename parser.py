import argparse


_method_list = ["mnistnet", "resnet", "resnet34", "densenet", "googlenet", "regnet", "transformer"]
_dataset_list = ["cifar10", "cifar100", "mnist", "wikitext2"]


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def gpu_list(v):
    if isinstance(v, int):
        return v
    elif ',' in v:
        return [int(g) for g in v.split(',')]
    else:
        raise argparse.ArgumentError("Accepts GPU Number or GPU list")


def dataset_list(v):
    if v not in _dataset_list:
        raise argparse.ArgumentError("Invalid dataset")
    return v


def model_list(v):
    if v not in _method_list:
        raise argparse.ArgumentError("Invalid model")
    return v


def get_parser():
    parser = argparse.ArgumentParser(description="Dynamic Batchsize for Distributed DNN Training")
    parser.add_argument('-debug', '--debug', type=str2bool, default=False, required=False,
                        help="Debug mode. Configure to True to run mnist and mnistnet with CPU. Default True.")
    parser.add_argument('-ws', '--world_size', type=int, default=4, required=False,
                        help="Configure the world size of the cluster. Default 4.")
    parser.add_argument('-b', '--batch_size', type=int, default=64, required=False,
                        help="Configure the batch size of the cluster. For example, a 512 batch size and 4 workers "
                             "will result in each work owns a batch size of 128. Default 64, recommended larger than "
                             "512.")
    parser.add_argument('-lr', '--learning_rate', type=float, default=0.01, required=False,
                        help="Configure the learning rate. Default 0.01.")
    parser.add_argument('-e', '--epoch_size', type=int, default=10, required=False,
                        help="Configure the epoch size of the training. Default 10.")
    parser.add_argument('-ds', '--dataset', type=dataset_list, default='wikitext2', required=False,
                        help="Configure target dataset, options are mnist, cifar10 and cifar100")
    parser.add_argument('-dbs', '--dynamic_batch_size', type=str2bool, default=True, required=False,
                        help="Dynamic Batch Size. Configure to True to enable. Default True.")
    parser.add_argument('-gpu', '--gpu', type=gpu_list, default=0, required=False,
                        help="Configure which gpu card to use, will not take effects in debug mode. "
                             "If you have multiple GPU cards, split it with comma. E.g. '0,0,0,1' with 4 workers will "
                             "result in "
                             "worker 0-2 to use GPU:0 and worker 3 to use GPU:1.")
    parser.add_argument('-m', '--model', type=model_list, default="transformer", required=False,
                        help="Configure the training model. Default ResNet-101. You can input resnet for ResNet-101, "
                             "densenet for DenseNet121, googlenet for GoogLeNet and regnet for RegNetY_400MF")
    parser.add_argument('-ft', '--fault_tolerance', type=str2bool, default=False, required=False,
                        help="Test the fault tolerance of DBS algorithm. If this is set to True, the artificial noice "
                             "will be added into the training process, which will randomly slow down some worker's "
                             "training speed. Default False.")
    parser.add_argument('-ftc', '--fault_tolerance_chance', type=float, default=0.1, required=False,
                        help="Configure how much chance there are for a worker to be slowed down. This option will "
                             "only takes effect when -ft is set to True. Default: 0.1.")
    parser.add_argument('-ocp', '--one_cycle_policy', type=str2bool, default=False, required=False,
                        help="Enable One Cycle Policy, which makes learning rate starts at 1/100 learning rate,"
                             "gradually increases to learning rate, and finally decreases to 1/100 learning rate at the"
                             "end.")
    parser.add_argument('-de', '--disable_enhancements', type=str2bool, default=False, required=False,
                        help="Temporary disable one cycle policy and dynamic weights. Only for testing. Do not enable"
                             "it unless you know what you are doing.")

    parser.add_argument('-seed', default=None, type=int,
                        help='seed for initializing training. ')
    parser.add_argument('-multiprocessing-distributed', action='store_true',
                        help='Use multi-processing distributed training to launch '
                             'N processes per node, which has N GPUs. This is the '
                             'fastest way to use PyTorch for either single node or '
                             'multi node data parallel training')
    parser.add_argument('-rank', default=-1, type=int,
                        help='node rank for distributed training')
    parser.add_argument('-dist-url', default='tcp://224.66.41.62:23456', type=str,
                        help='url used to set up distributed training')
    parser.add_argument('-dist-backend', default='nccl', type=str,
                        help='distributed backend')
    parser.add_argument('-log-dir', default=None, type=str,
                        help='log directory path')
    return parser
