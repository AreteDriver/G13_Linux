from .device import open_g13, read_event
from .mapper import G13Mapper


def main():
    print("Opening Logitech G13…")
    h = open_g13()
    mapper = G13Mapper()
    print("G13 opened. Press keys; Ctrl+C to exit.")

    try:
        while True:
            data = read_event(h)
            if data:
                mapper.handle_raw_report(data)
    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        h.close()
        mapper.close()


if __name__ == "__main__":
    main()
