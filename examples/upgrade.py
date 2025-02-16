# pylint: disable=W0621
"""Asynchronous Python client for WLED."""

import asyncio
import sys

from wled import WLED, WLEDReleases


async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python upgrade.py <ip_address>")
        sys.exit(1)

    """Show example on upgrade your WLED device."""
    async with WLED(sys.argv[1]) as led:
        device = await led.update()
        print(f"Current version: {device.info.version}")

        async with WLEDReleases() as releases:
            latest = await releases.releases(device.info)
            print(f"Latest stable version: {latest.stable}")
            print(f"Latest beta version: {latest.beta}")

        if not latest.stable:
            print("No stable version found")
            return

        print("Upgrading WLED....")
        await led.upgrade(version=latest.beta)

        print("Waiting for WLED to come back....")
        await asyncio.sleep(5)

        device = await led.update()
        print(f"Current version: {device.info.version}")


if __name__ == "__main__":
    asyncio.run(main())
