"""Start the table and leave it up. Caleb plays while this runs."""

import argparse
import os

from dcc_engine.server import make_server


def main(argv=None):
    parser = argparse.ArgumentParser(description="Shooting Gallery table. Localhost only unless you set the host.")
    parser.add_argument("--host", default=os.environ.get("DCC_TABLE_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("DCC_TABLE_PORT", "8765")))
    parser.add_argument("--party-size", type=int, default=2, choices=(2, 3, 4))
    args = parser.parse_args(argv)
    httpd = make_server(args.host, args.port, party_size=args.party_size)
    host, port = httpd.server_address[:2]
    print(f"player  http://{host}:{port}/player", flush=True)
    print(f"table   http://{host}:{port}/gm", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("table stopped", flush=True)
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
