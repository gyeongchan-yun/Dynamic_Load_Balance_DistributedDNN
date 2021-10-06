import logging, socket, os

# Log-Related Variables

def init_logger(args, rank, basefile_name, output_dir="./logs"):

    os.makedirs(output_dir, exist_ok=True)

    extra = {
        "world_size": args.world_size,
        "lr": args.lr,
        "dbs": "enabled" if args.dbs_enabled else "disabled",
        "ft": "enabled" if args.fault_tolerance else "disabled"
    }

    logger = logging.getLogger(socket.gethostname())
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s [%(world_size)s:%(lr)s:dbs_%(dbs)s:ft_%(ft)s] [%(filename)s:%(lineno)d] %(levelname)s %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    log_filename = basefile_name.format(str(rank)) + ".log"
    log_file = os.path.join(output_dir, log_filename)
    fh = logging.FileHandler(log_file, 'w+')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger = logging.LoggerAdapter(logger, extra)
    return logger
