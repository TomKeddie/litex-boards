#!/usr/bin/env python3

import argparse

from migen import *

from litex_boards.platforms import arcticserdes
from litex.soc.cores import *
from litex.soc.integration import soc_core
from litex.soc.cores import gpio
from litex.soc.integration.builder import *

# Build --------------------------------------------------------------------------------------------

def main():
    platform = arcticserdes.Platform()
    sys_clk_freq = 1/platform.default_clk_period*1e9
    soc = soc_core.SoCCore(platform,
                           sys_clk_freq,
                           cpu_variant="lite",
                           integrated_rom_size=0x8000,
                           integrated_sram_size=0x8000)
    
    led_pad = platform.request("user_led")
    soc.submodules.leds = gpio.GPIOOut(led_pad)
    soc.add_csr("leds")
    builder = Builder(soc)
    builder.build()


if __name__ == "__main__":
    main()
