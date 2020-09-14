def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def main(top_block_cls=bercurve_generator, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(fc=options.fc, mx=options.mx, my=options.my, n=options.n)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    """try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()"""
    while is_empty(tb.blocks_vector_sink_x_0.data()):
        pass

    if is_empty(tb.blocks_vector_sink_x_0.data()) == False:
        print("in:", tb.blocks_vector_sink_x_0_0.data())
        print("out:", tb.blocks_vector_sink_x_0.data())
        print(len(tb.blocks_vector_sink_x_0_0.data()))
        print(len(tb.blocks_vector_sink_x_0.data()))


if __name__ == "__main__":
    main()
